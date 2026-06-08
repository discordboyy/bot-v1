import random

async def game(update, context):
    result = random.randint(1, 10)

    if result <= 7:
        await update.message.reply_text(
            f"Ты отбил мяч! Выпало {result}"
        )
    else:
        await update.message.reply_text(
            f"Промах! Выпало {result}"
        )
