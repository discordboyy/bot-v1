from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def shop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
text = """
```

🛍 <b>Makki Shop</b>

━━━━━━━━━━━━━━

💻 <b>Digital Services</b>

🌐 Landing Website
💰 5,000 – 10,000 NOK

🚀 MVP / Prototype
💰 15,000 – 30,000 NOK

⚙️ Web Application
💰 25,000 – 50,000 NOK

🛠 Technical Support
💰 300 – 600 NOK / hour

🎯 Consultation
💰 Free / 200 – 400 NOK

🧪 Experimental Projects
💰 By agreement

━━━━━━━━━━━━━━

🎁 <b>Rewards Store</b>

✍️ Founder Autograph
💵 $100
🔒 Available soon

🎮 Discord Nitro (1 Month)
🏆 10,000 Makki Points

🎮 Discord Nitro (3 Months)
🏆 25,000 Makki Points

👕 Makki Merch
🏆 50,000 Makki Points

🎨 Exclusive Digital Art
🏆 15,000 Makki Points

🚀 VIP Community Access
🏆 75,000 Makki Points

━━━━━━━━━━━━━━

👤 Your Account

💰 Balance: 0 MKK
🏆 Points: 0

⚠️ Point system is currently unavailable.
Rewards and economy features will arrive in a future update.

━━━━━━━━━━━━━━

🌍 Makki

Growth • Creativity • Innovation

📧 [makki.creative@gmail.com](mailto:makki.creative@gmail.com)
"""

```
await update.message.reply_text(
    text,
    parse_mode="HTML"
)
```

shop_handler = CommandHandler(
"shop",
shop_command
)
