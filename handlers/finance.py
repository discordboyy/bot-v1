import asyncio
import httpx
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def finance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=10) as client:

            forex_task = client.get(
                "https://api.frankfurter.app/latest",
                params={
                    "base": "USD",
                    "symbols": "EUR,NOK,UAH"
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

        usd_eur = forex_data["rates"]["EUR"]
        usd_nok = forex_data["rates"]["NOK"]
        usd_uah = forex_data["rates"]["UAH"]

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

<b>Forex</b>
USD → EUR: <b>{usd_eur:.4f}</b>
USD → NOK: <b>{usd_nok:.4f}</b>
USD → UAH: <b>{usd_uah:.4f}</b>

━━━━━━━━━━━━━━

<b>₿ Crypto (24h)</b>

BTC: <b>${btc_price:,.2f}</b>
{fmt_change(btc_change)}

ETH: <b>${eth_price:,.2f}</b>
{fmt_change(eth_change)}

BNB: <b>${bnb_price:,.2f}</b>
{fmt_change(bnb_change)}

━━━━━━━━━━━━━━
Makki System
"""

        await update.message.reply_text(
            text,
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
