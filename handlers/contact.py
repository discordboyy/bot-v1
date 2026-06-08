from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


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

© 2025 Makki. All rights reserved.
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


contact_handler = CommandHandler("contact", contact_command)