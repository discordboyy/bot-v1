from telegram.ext import Application

from handlers.start import start
from handlers.ping import ping
from handlers.game import game

from telegram.ext import CommandHandler

TOKEN = "YOUR_TOKEN"

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("game", game))

app.run_polling()
