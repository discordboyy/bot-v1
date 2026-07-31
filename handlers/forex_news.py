# handlers/forex_news.py
"""
Экономический календарь Forex Factory -> отправка High-impact новостей в Telegram.

Портировано из bot-v0.1 (parse.py + webhook.py), но:
- вместо Discord webhook -> отправка через context.bot.send_message (Telegram)
- вместо requests (sync) -> httpx (async), чтобы не блокировать event loop бота
- вместо pytz -> zoneinfo (стандартная библиотека, ничего доп. ставить не надо)
- добавлен пропуск выходных (суббота/воскресенье)
- работает и как команда /forexnews (ручной запуск), и как job в scheduler.py (авто)
"""
import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import os

import httpx
from dateutil import parser as date_parser
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

logger = logging.getLogger(__name__)

FEED_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
FEED_URL_MIRROR = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json"

SOURCE_TZ = ZoneInfo("America/New_York")   # таймзона, в которой отдаёт фид
TARGET_TZ = ZoneInfo("Europe/Oslo")        # таймзона для отображения времени

# ID канала, куда уходит автоматическая рассылка (тот же, что в scheduler.py)
load_dotenv()

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
}

IMPACT_ORDER = {"Low": 0, "Medium": 1, "High": 2, "Holiday": -1}
IMPACT_EMOJI = {"Low": "🟢", "Medium": "🟡", "High": "🔴", "Holiday": "⚪"}


def is_weekend(target_date: date) -> bool:
    """Суббота = 5, воскресенье = 6 (datetime.weekday())."""
    return target_date.weekday() >= 5


async def fetch_calendar(client: httpx.AsyncClient) -> list[dict]:
    """Скачивает недельный календарь и возвращает события со временем в TARGET_TZ."""
    try:
        resp = await client.get(FEED_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except httpx.HTTPError:
        resp = await client.get(FEED_URL_MIRROR, headers=HEADERS, timeout=10)
        resp.raise_for_status()

    raw_events = resp.json()

    events = []
    for e in raw_events:
        # пример поля e['date']: "07-28-2026 8:30am"
        dt = date_parser.parse(e["date"])
        dt = dt.replace(tzinfo=SOURCE_TZ) if dt.tzinfo is None else dt
        dt_local = dt.astimezone(TARGET_TZ)

        events.append({
            "title": e.get("title"),
            "country": e.get("country"),
            "impact": e.get("impact"),  # Low / Medium / High / Holiday
            "forecast": e.get("forecast"),
            "previous": e.get("previous"),
            "datetime": dt_local,
        })

    return events


def events_for_day(events: list[dict], target_date: date, min_impact: str = "High") -> list[dict]:
    threshold = IMPACT_ORDER.get(min_impact, 2)
    result = [
        e for e in events
        if e["datetime"].date() == target_date
        and IMPACT_ORDER.get(e["impact"], -1) >= threshold
    ]
    result.sort(key=lambda e: e["datetime"])
    return result


def build_forex_news_text(events: list[dict], target_date: date) -> str:
    header = f"<b>Forex Factory — High Impact новости на {target_date.strftime('%d.%m.%Y')}</b>"

    if not events:
        return f"{header}\n\n━━━━━━━━━━━━━━\n\nНа этот день High-impact новостей нет."

    lines = [header, "", "━━━━━━━━━━━━━━", ""]

    for e in events:
        time_str = e["datetime"].strftime("%H:%M")
        emoji = IMPACT_EMOJI.get(e["impact"], "🔴")
        title = html.escape(str(e.get("title") or ""))
        country = html.escape(str(e.get("country") or ""))
        lines.append(f"{emoji} <b>{time_str}</b> — [{country}] {title}")

        extra = []
        forecast = e.get("forecast")
        previous = e.get("previous")
        if forecast:
            extra.append(f"Прогноз: {html.escape(str(forecast))}")
        if previous:
            extra.append(f"Пред.: {html.escape(str(previous))}")
        if extra:
            lines.append("   " + " | ".join(extra))
        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    lines.append('<a href="https://makki.no">Makki System</a>')

    return "\n".join(lines)


async def _fetch_and_build(target_date: date, min_impact: str = "High") -> str:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        events = await fetch_calendar(client)
    day_events = events_for_day(events, target_date, min_impact=min_impact)
    return build_forex_news_text(day_events, target_date)


# ─────────────────────────────────────────
# АВТО-РАССЫЛКА (вызывается из scheduler.py)
# ─────────────────────────────────────────

async def send_forex_news(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(TARGET_TZ).date()

    if is_weekend(today):
        logger.info("Forex news: today is weekend, skipping (%s)", today)
        return

    try:
        text = await _fetch_and_build(today, min_impact="High")
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        logger.info("Forex news sent for %s.", today)
    except Exception as e:
        logger.error("Forex news scheduler error: %s", e)


# ─────────────────────────────────────────
# РУЧНАЯ КОМАНДА /forexnews (для проверки в любой день, включая выходные)
# ─────────────────────────────────────────

async def forexnews_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(TARGET_TZ).date()
    try:
        text = await _fetch_and_build(today, min_impact="High")
        if is_weekend(today):
            text += "\n\n<i>(Сегодня выходной — автоматическая рассылка в канал в этот день пропускается, это ручной предпросмотр.)</i>"
        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        await update.message.reply_text(f"❌ Forex news error:\n{e}")


forex_news_handler = CommandHandler(
    ["forexnews", "forex"],
    forexnews_command
)
