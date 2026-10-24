import os
import json
import html
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────
TZ = ZoneInfo("Europe/Oslo")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.getenv("EPIC_CACHE_PATH", os.path.join(BASE_DIR, "data", "epic_deals.json"))
MAX_AGE_DAYS = 8  # older file = expired discounts, don't post
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


# ─────────────────────────────────────────
# CACHE (file is uploaded from the PC, see tools/epic_fetch_local.py)
# ─────────────────────────────────────────
def load_cache():
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Epic: cache not readable ({e}).")
        return None


def _too_old(cache):
    try:
        fetched = datetime.fromisoformat(cache["fetched_at"])
    except (KeyError, ValueError):
        return True
    if fetched.tzinfo is None:
        fetched = fetched.replace(tzinfo=TZ)
    return datetime.now(TZ) - fetched > timedelta(days=MAX_AGE_DAYS)


# ─────────────────────────────────────────
# DAILY POST (09:00)
# ─────────────────────────────────────────
async def send_epic_deal(context):
    cache = load_cache()
    if not cache or not cache.get("deals"):
        logger.warning("Epic: no deals to post.")
        return
    if _too_old(cache):
        logger.warning(
            f"Epic: cache is older than {MAX_AGE_DAYS} days "
            f"({cache.get('fetched_at')}), skipping post. Is the PC upload running?"
        )
        return

    deals = cache["deals"]
    deal = deals[datetime.now(TZ).weekday() % len(deals)]  # Mon=0 ... Sun=6

    title = html.escape(deal["title"])
    url = html.escape(deal["url"], quote=True)
    caption = (
        "<b>🎮 Epic Games Deal of the Day</b>\n\n"
        f"<b>{title}</b>\n"
        f"🔥 <b>-{deal['percent']}%</b>\n"
        f"<s>{html.escape(deal['original_price'])}</s> → "
        f"<b>{html.escape(deal['discount_price'])}</b>\n\n"
        f'<a href="{url}">Open in Epic Games Store</a>'
    )

    try:
        if deal.get("image"):
            await context.bot.send_photo(
                chat_id=CHANNEL_ID, photo=deal["image"],
                caption=caption, parse_mode="HTML",
            )
        else:
            await context.bot.send_message(
                chat_id=CHANNEL_ID, text=caption, parse_mode="HTML"
            )
        logger.info(f"Epic deal sent: {deal['title']}")
    except Exception as e:
        logger.error(f"Epic send error: {e}")
