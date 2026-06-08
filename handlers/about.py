# handlers/about.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

```
text = """
```

🌍 <b>About Makki</b>

━━━━━━━━━━━━━━

Makki is a modern digital brand founded by <b>Makar Hrydkovets (Mertygraal)</b>.

The project combines creativity,
technology, entrepreneurship and
continuous self-development into a
single evolving ecosystem.

━━━━━━━━━━━━━━

🎯 <b>Mission</b>

To build in public.

Makki openly shares ideas,
experiments, projects, progress,
successes and failures.

The goal is not perfection —
the goal is growth.

━━━━━━━━━━━━━━

🚀 <b>What Makki Creates</b>

• Websites
• Web Applications
• MVP Products
• Digital Solutions
• Creative Concepts
• Open Source Projects
• Experiments & Prototypes

━━━━━━━━━━━━━━

💡 <b>Core Values</b>

✨ Creativity
📈 Growth
🔍 Transparency
⚡ Innovation
🤝 Community

━━━━━━━━━━━━━━

🌐 <b>Vision</b>

To grow from a personal digital brand
into an international ecosystem with:

• Online Services
• Digital Products
• Creative Communities
• Physical Spaces
• Innovation Hubs

━━━━━━━━━━━━━━

🛍 Use /shop to explore services
📊 Use /finance for market updates
📩 Use /contact to get in touch

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

about_handler = CommandHandler(
"about",
about_command
)
