from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def project_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
text = """
```

🚀 <b>Makki Project</b>

━━━━━━━━━━━━━━

🌍 <b>What is Makki?</b>

Makki is a digital ecosystem built around:
• creativity
• technology
• entrepreneurship
• continuous growth

It is not just a product —
it is an evolving system.

━━━━━━━━━━━━━━

🧠 <b>Current Stage</b>

📦 Version: v1 (Early Build)
⚙️ Status: Active Development
🌐 Mode: Build in Public

We are actively building:
• Telegram Bot
• Web Platform
• Service Ecosystem
• Internal Economy System

━━━━━━━━━━━━━━

🧩 <b>Modules</b>

🤖 Bot System
→ Telegram interface for users

💹 Finance Module
→ Forex + Crypto tracking

🛍 Shop System
→ Services & digital rewards

🎮 Game Layer (coming soon)
→ Casino, XP, Levels, Rewards

💰 Economy Layer (coming soon)
→ Balance, points, rewards system

━━━━━━━━━━━━━━

📈 <b>Vision</b>

Makki will evolve into:

• Global digital brand
• Creative tech ecosystem
• Service marketplace
• Community-driven platform

━━━━━━━━━━━━━━

📡 <b>Status</b>

🟢 Bot: Online
🟡 Economy: In development
🔴 Casino: Not active yet
🟢 Finance: Active (basic version)
🟢 Shop: Active (demo version)

━━━━━━━━━━━━━━

📩 Contact:
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

project_handler = CommandHandler(
"project",
project_command
)
