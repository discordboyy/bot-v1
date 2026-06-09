# handlers/finance.py
import asyncio
import httpx
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki.png"


BINANCE_URL = "https://api.binance.com/api/v3/ticker/24hr"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


async def finance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:

            # -------------------------
            # 1) FOREX (Frankfurter)
            # -------------------------
            forex_task = client.get(
                "https://api.frankfurter.dev/v1/latest",
                params={"base": "USD", "symbols": "EUR,GBP,NOK"}
            )

            # -------------------------
            # 2) CRYPTO BINANCE BATCH
            # -------------------------
            binance_task = client.get(
                BINANCE_URL,
                params={"symbols": '["BTCUSDT","ETHUSDT","BNBUSDT"]'}
            )

            forex_resp, binance_resp = await asyncio.gather(
                forex_task,
                binance_task,
                return_exceptions=True
            )

            # -------------------------
            # FOREX обработка
            # -------------------------
            forex_data = {}
            try:
                if isinstance(forex_resp, httpx.Response):
                    forex_resp.raise_for_status()
                    forex_data = forex_resp.json()
            except Exception:
                forex_data = {}

            rates = forex_data.get("rates", {})

            usd_eur = rates.get("EUR", 0)
            usd_gbp = rates.get("GBP", 0)
            usd_nok = rates.get("NOK", 0)

            eur_usd = 1 / usd_eur if usd_eur else 0
            gbp_usd = 1 / usd_gbp if usd_gbp else 0

            # -------------------------
            # CRYPTO BINANCE PARSE
            # -------------------------
            crypto_data = None

            try:
                if isinstance(binance_resp, httpx.Response):
                    binance_resp.raise_for_status()
                    crypto_data = binance_resp.json()
            except Exception:
                crypto_data = None

            # -------------------------
            # FALLBACK COINGECKO
            # -------------------------
            if not crypto_data:
                try:
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
                        "BTCUSDT": {
                            "price": cg["bitcoin"]["usd"],
                            "change": cg["bitcoin"]["usd_24h_change"]
                        },
                        "ETHUSDT": {
                            "price": cg["ethereum"]["usd"],
                            "change": cg["ethereum"]["usd_24h_change"]
                        },
                        "BNBUSDT": {
                            "price": cg["binancecoin"]["usd"],
                            "change": cg["binancecoin"]["usd_24h_change"]
                        }
                    }

                except Exception:
                    raise Exception("Both Binance and CoinGecko failed")

            else:
                # Binance success parsing
                crypto = {
                    item["symbol"]: {
                        "price": float(item["lastPrice"]),
                        "change": float(item["priceChangePercent"])
                    }
                    for item in crypto_data
                }

            # -------------------------
            # VALUES
            # -------------------------
            btc_price = crypto["BTCUSDT"]["price"]
            btc_change = crypto["BTCUSDT"]["change"]

            eth_price = crypto["ETHUSDT"]["price"]
            eth_change = crypto["ETHUSDT"]["change"]

            bnb_price = crypto["BNBUSDT"]["price"]
            bnb_change = crypto["BNBUSDT"]["change"]

            def fmt_change(value):
                return f"+{value:.2f}%" if value >= 0 else f"{value:.2f}%"

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
<a href="https://makki.no">Makki System</a>
"""

            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=PHOTO_URL,
                caption=text,
                parse_mode="HTML"
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Finance API error:\n{e}"
        )


finance_handler = CommandHandler("finance", finance_command)