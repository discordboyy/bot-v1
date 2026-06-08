# bot.py
import os
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()

from handlers.start import start
from handlers.ping import ping
from handlers.game import game
from handlers.finance import finance_handler
from handlers.about import about_handler
from handlers.contact import contact_handler
from handlers.help import help_handler
from handlers.shop import shop_handler
from handlers.project import project_handler

TOKEN = os.getenv("BOT_TOKEN")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("game", game))
    app.add_handler(finance_handler)
    app.add_handler(about_handler)
    app.add_handler(contact_handler)
    app.add_handler(help_handler)
    app.add_handler(shop_handler)
    app.add_handler(project_handler)

    print("Bot is running...")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()