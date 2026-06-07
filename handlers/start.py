async def start(update, context):
    await update.message.reply_text(
        "Бот работает. Команды: /ping, /game"
    )
