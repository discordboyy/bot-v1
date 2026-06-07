import asyncio
import os

from telegram.ext import Application, CommandHandler

from handlers.start import start
from handlers.ping import ping
from handlers.game import game

TOKEN = os.environ["BOT_TOKEN"]

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("game", game))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
