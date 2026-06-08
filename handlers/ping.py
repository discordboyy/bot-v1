# handlers/ping.py
async def ping(update, context):
    await update.message.reply_text("Pong! Бот работает.")