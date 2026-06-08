from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import httpx


async def finance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=10) as client:

            forex = await client.get(
                "https://api.frankfurter.app/latest?base=USD&symbols=EUR,NOK,UAH"
            )
            forex_data = forex.json()

            usd_eur = forex_data["rates"]["EUR"]
            usd_nok = forex_data["rates"]["NOK"]
            usd_uah = forex_data["rates"]["UAH"]

            btc = await client.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
            eth = await client.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
            bnb = await client.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT")

            btc_price = float(btc.json()["price"])
            eth_price = float(eth.json()["price"])
            bnb_price = float(bnb.json()["price"])

        text = f"""
    <b>Makki Finance</b>

    <b>Forex</b>
    USD → EUR: <b>{usd_eur}</b>
    USD → NOK: <b>{usd_nok}</b>
    USD → UAH: <b>{usd_uah}</b>

    ━━━━━━━━━━━━━━

    <b>Crypto</b>
    BTC: <b>${btc_price:,.2f}</b>
    ETH: <b>${eth_price:,.2f}</b>
    BNB: <b>${bnb_price:,.2f}</b>

    ━━━━━━━━━━━━━━
    Makki System
    """

        await update.message.reply_text(text, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(
            f"Finance service unavailable\n{e}"
        )


finance_handler = CommandHandler("finance", finance_command)