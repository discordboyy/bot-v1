from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki-v4.png"

async def project_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """<b>Makki Project</b>

━━━━━━━━━━━━━━

    <b>What is Makki?</b>

Makki is a digital ecosystem built around creativity, technology, entrepreneurship and continuous growth.

━━━━━━━━━━━━━━

    <b>Current Stage</b>

    Version: v1 (Early Build)
    Status: Active Development
    Mode: Build in Public

━━━━━━━━━━━━━━

    <b>Modules</b>

    Bot System — Telegram interface
    Finance Module — Forex + Crypto
    Shop System — Services and rewards
    Game Layer — coming soon
    Economy Layer — coming soon

━━━━━━━━━━━━━━

    <b>Status</b>

    Bot: Online
    Finance: Active
    Shop: Active (demo)
    Economy: In development
    Casino: Not active yet

━━━━━━━━━━━━━━

makki.creative@gmail.com

© 2025–2026 Makki — Growth • Creativity • Innovation"""

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=PHOTO_URL,
        caption=text,
        parse_mode="HTML",
    )

project_handler = CommandHandler("project", project_command)