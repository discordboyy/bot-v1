from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
text = """
```

❓ <b>Makki Help Center</b>

━━━━━━━━━━━━━━

🤖 <b>Available Commands</b>

🏠 /start
Open the main welcome message.

🌍 /about
Learn more about Makki and its mission.

📩 /contact
Contact information and support.

🛍 /shop
Browse available services and rewards.

📈 /finance
Forex and cryptocurrency market data.

🏓 /ping
Check if the bot is online.

❓ /help
Display this help menu.

━━━━━━━━━━━━━━

💡 <b>Coming Soon</b>

💰 Balance System
🎁 Daily Rewards
📊 Levels & XP
🏆 Leaderboards

🎰 Casino
🎲 Slots
🪙 Coin Flip
🎡 Roulette

━━━━━━━━━━━━━━

🌍 <b>About Makki</b>

Makki is a digital ecosystem focused on:

• Creativity
• Development
• Technology
• Innovation
• Open Building

━━━━━━━━━━━━━━

📧 Support

[makki.creative@gmail.com](mailto:makki.creative@gmail.com)

━━━━━━━━━━━━━━

© 2025–2026 Makki

Growth • Creativity • Innovation
"""

```
await update.message.reply_text(
    text,
    parse_mode="HTML"
)
```

help_handler = CommandHandler(
"help",
help_command
)
