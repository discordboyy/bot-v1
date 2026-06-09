import logging
import asyncio
import httpx
from telegram.ext import Application

logger = logging.getLogger(__name__)

CHANNEL_ID = -1001997933600

SHOP_PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki-v2.png"
FINANCE_PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki.png"
BINANCE_URL = "https://api.binance.com/api/v3/ticker/24hr"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


# ─────────────────────────────────────────
# FINANCE — каждые 3 дня
# ─────────────────────────────────────────

async def send_finance_update(context):
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:

            forex_task = client.get(
                "https://api.frankfurter.dev/v1/latest",
                params={"base": "USD", "symbols": "EUR,GBP,NOK"}
            )
            binance_task = client.get(
                BINANCE_URL,
                params={"symbols": '["BTCUSDT","ETHUSDT","BNBUSDT"]'}
            )

            forex_resp, binance_resp = await asyncio.gather(
                forex_task, binance_task, return_exceptions=True
            )

            rates = {}
            try:
                if isinstance(forex_resp, httpx.Response):
                    forex_resp.raise_for_status()
                    rates = forex_resp.json().get("rates", {})
            except Exception:
                pass

            usd_eur = rates.get("EUR", 0)
            usd_gbp = rates.get("GBP", 0)
            usd_nok = rates.get("NOK", 0)
            eur_usd = 1 / usd_eur if usd_eur else 0
            gbp_usd = 1 / usd_gbp if usd_gbp else 0

            crypto = {}
            try:
                if isinstance(binance_resp, httpx.Response):
                    binance_resp.raise_for_status()
                    data = binance_resp.json()
                    crypto = {
                        item["symbol"]: {
                            "price": float(item["lastPrice"]),
                            "change": float(item["priceChangePercent"])
                        }
                        for item in data
                    }
            except Exception:
                pass

            if not crypto:
                cg_resp = await client.get(
                    COINGECKO_URL,
                    params={
                        "ids": "bitcoin,ethereum,binancecoin",
                        "vs_currencies": "usd",
                        "include_24hr_change": "true"
                    }
                )
                cg_resp.raise_for_status()
                cg = cg_resp.json()
                crypto = {
                    "BTCUSDT": {"price": cg["bitcoin"]["usd"],     "change": cg["bitcoin"]["usd_24h_change"]},
                    "ETHUSDT": {"price": cg["ethereum"]["usd"],    "change": cg["ethereum"]["usd_24h_change"]},
                    "BNBUSDT": {"price": cg["binancecoin"]["usd"], "change": cg["binancecoin"]["usd_24h_change"]},
                }

            def fmt_change(value):
                return f"+{value:.2f}%" if value >= 0 else f"{value:.2f}%"

            btc_price  = crypto["BTCUSDT"]["price"]
            btc_change = crypto["BTCUSDT"]["change"]
            eth_price  = crypto["ETHUSDT"]["price"]
            eth_change = crypto["ETHUSDT"]["change"]
            bnb_price  = crypto["BNBUSDT"]["price"]
            bnb_change = crypto["BNBUSDT"]["change"]

            text = f"""
<b>Makki Finance</b>

<b>💵 Forex</b>
EUR/USD: <b>{eur_usd:.4f}</b>
GBP/USD: <b>{gbp_usd:.4f}</b>
USD/NOK: <b>{usd_nok:.4f}</b>

━━━━━━━━━━━━━━

<b>₿ Crypto (24h)</b>

BTC: ${btc_price:,.2f} - {fmt_change(btc_change)}

ETH: ${eth_price:,.2f} - {fmt_change(eth_change)}

BNB: ${bnb_price:,.2f} - {fmt_change(bnb_change)}

━━━━━━━━━━━━━━
<a href="https://makki.no">Makki System</a>"""

            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=FINANCE_PHOTO_URL,
                caption=text,
                parse_mode="HTML"
            )
            logger.info("Finance update sent.")

    except Exception as e:
        logger.error(f"Finance scheduler error: {e}")


# ─────────────────────────────────────────
# SHOP — каждые 14 дней
# ─────────────────────────────────────────

async def send_shop_update(context):
    text = """<b>Makki Shop 🎧</b>

━━━━━━━━━━━━━━

    <b>Digital Services</b>

    Landing Website
    5,000 – 10,000 NOK

    MVP / Prototype
    15,000 – 30,000 NOK

    Web Application
    25,000 – 50,000 NOK

    Technical Support
    300 – 600 NOK / hour

    Consultation
    Free / 200 – 400 NOK

━━━━━━━━━━━━━━

    <b>Rewards Store</b>

    Founder Autograph — $100
    Available soon

    Discord Nitro (1 Month) — 10,000 pts
    Discord Nitro (3 Months) — 25,000 pts
    Makki Merch — 50,000 pts
    Exclusive Digital Art — 15,000 pts
    VIP Community Access — 75,000 pts

━━━━━━━━━━━━━━

    Point system is currently unavailable.
    Rewards will arrive in a future update.

━━━━━━━━━━━━━━

    makki.creative@gmail.com

© 2025–2026 <a href="https://makki.no">Makki</a> — Growth • Creativity • Innovation"""

    try:
        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=SHOP_PHOTO_URL,
            caption=text,
            parse_mode="HTML"
        )
        logger.info("Shop update sent.")
    except Exception as e:
        logger.error(f"Shop scheduler error: {e}")


# ─────────────────────────────────────────
# РЕГИСТРАЦИЯ ЗАДАЧ
# ─────────────────────────────────────────

def setup_scheduler(app: Application):
    job_queue = app.job_queue

    job_queue.run_repeating(
        send_finance_update,
        interval=3 * 24 * 60 * 60,
        first=10,
        name="finance_update"
    )

    job_queue.run_repeating(
        send_shop_update,
        interval=14 * 24 * 60 * 60,
        first=20,
        name="shop_update"
    )

    logger.info("Scheduler jobs registered.")