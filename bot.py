import os
from telegram.ext import Application, CommandHandler

from handlers.start import start
from handlers.ping import ping
from handlers.game import game

TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = Application.builder().token(TOKEN).build()

    # handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("game", game))

    print("Bot is running...")

    # ❗ правильный запуск (BLOCKING)
    app.run_polling()


if __name__ == "__main__":
    main()