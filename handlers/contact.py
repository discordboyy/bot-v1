from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki.png"

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
<b>Makki Contact Center</b>

Makki — digital brand focused on creativity, development and innovation.

Founder:
Makar Hrydkovets (Mertygraal)

Email:
makki.creative@gmail.com

About Makki:
A platform documenting growth, creation, technology, design and entrepreneurship in public.

Socials:
• Instagram
• X (Twitter)
• Discord
• YouTube
• Telegram

Future Vision:
Building an international ecosystem of creative projects, digital products, communities and innovation hubs.

© 2025 <a href="https://makki.no"Makki</a>. All rights reserved.
"""

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=PHOTO_URL,
        caption=text,
        parse_mode="HTML",
    )


contact_handler = CommandHandler("contact", contact_command)