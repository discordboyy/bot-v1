import os
from telegram.ext import Application, CommandHandler

from handlers.start import start
from handlers.ping import ping
from handlers.game import game
from handlers.finance import finance_handler

TOKEN = os.getenv("BOT_TOKEN")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    # handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("game", game))

    # finance
    app.add_handler(finance_handler)

    print("Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()