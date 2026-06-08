import asyncio
import httpx
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki.png"

async def finance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(
            timeout=10,
            follow_redirects=True
        ) as client:

            forex_task = client.get(
                "https://api.frankfurter.dev/v1/latest",
                params={
                    "base": "USD",
                    "symbols": "EUR,GBP,NOK"
                }
            )

            crypto_task = client.get(
                "https://api.binance.com/api/v3/ticker/24hr",
                params={
                    "symbols": '["BTCUSDT","ETHUSDT","BNBUSDT"]'
                }
            )

            forex_resp, crypto_resp = await asyncio.gather(
                forex_task,
                crypto_task
            )

            forex_resp.raise_for_status()
            crypto_resp.raise_for_status()

        forex_data = forex_resp.json()
        crypto_data = crypto_resp.json()

        rates = forex_data["rates"]

        usd_eur = rates["EUR"]
        usd_gbp = rates["GBP"]
        usd_nok = rates["NOK"]
        
        eur_usd = 1 / usd_eur
        gbp_usd = 1 / usd_gbp

        crypto = {
            item["symbol"]: {
                "price": float(item["lastPrice"]),
                "change": float(item["priceChangePercent"])
            }
            for item in crypto_data
        }

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
Makki System
"""

        await update.message.reply_photo(
            photo=PHOTO_URL,
            caption=text,
            parse_mode="HTML"
        )

    except httpx.HTTPError as e:
        await update.message.reply_text(
            f"❌ Finance API error:\n{e}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Finance service unavailable:\n{e}"
        )


finance_handler = CommandHandler("finance", finance_command)
