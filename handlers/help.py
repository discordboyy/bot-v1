from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """❓ <b>Makki Help Center</b>

━━━━━━━━━━━━━━

🤖 <b>Available Commands</b>

/start — Main welcome message
/about — About Makki
/project — Project overview
/shop — Services and rewards
/finance — Forex and crypto data
/contact — Contact information
/ping — Check if bot is online
/help — This menu

━━━━━━━━━━━━━━

💡 <b>Coming Soon</b>

💰 Balance System
🎁 Daily Rewards
📊 Levels and XP
🎰 Casino (Slots, Coinflip, Roulette)

━━━━━━━━━━━━━━

📧 makki.creative@gmail.com

© 2025–2026 Makki — Growth • Creativity • Innovation"""

    await update.message.reply_text(text, parse_mode="HTML")

help_handler = CommandHandler("help", help_command)