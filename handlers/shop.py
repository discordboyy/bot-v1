from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki-v2.png"

async def shop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """<b>Makki Shop</b>

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

© 2025–2026 Makki — Growth • Creativity • Innovation"""

    await update.message.reply_text(
        photo=PHOTO_URL,
        caption=text,
        parse_mode="HTML"
    )

shop_handler = CommandHandler("shop", shop_command)