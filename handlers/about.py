from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki.png"

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """<b>About Makki</b>

━━━━━━━━━━━━━━

Makki is a modern digital brand founded by <b>Makar Hrydkovets (Mertygraal)</b>.

The project combines creativity, technology, entrepreneurship and continuous self-development into a single evolving ecosystem.

━━━━━━━━━━━━━━

    <b>Mission</b>

To build in public. Makki openly shares ideas, experiments, projects, progress, successes and failures.

The goal is not perfection — the goal is growth.

━━━━━━━━━━━━━━

    <b>What Makki Creates</b>

- Websites
- Web Applications
- MVP Products
- Digital Solutions
- Creative Concepts
- Open Source Projects

━━━━━━━━━━━━━━

    <b>Core Values</b>

    Creativity
    Growth
    Transparency
    Innovation
    Community

━━━━━━━━━━━━━━


© 2025–2026 Makki — Growth • Creativity • Innovation"""

    keyboard = [
        [InlineKeyboardButton("🛍 Explore Services", callback_data="cmd_shop")],
        [InlineKeyboardButton("📈 Market Updates", callback_data="cmd_finance")],
        [InlineKeyboardButton("📩 Get in Touch", callback_data="cmd_contact")],
    ]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=PHOTO_URL,
        caption=text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

about_handler = CommandHandler("about", about_command)