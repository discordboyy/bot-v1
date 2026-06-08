from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

HELP_TEXT = """<b>Makki — Command Center</b>

━━━━━━━━━━━━━━

Choose a section below or type any command directly."""

BUTTONS = [
    [
        InlineKeyboardButton("Start", callback_data="cmd_start"),
        InlineKeyboardButton("About", callback_data="cmd_about"),
    ],
    [
        InlineKeyboardButton("Project", callback_data="cmd_project"),
        InlineKeyboardButton("Shop", callback_data="cmd_shop"),
    ],
    [
        InlineKeyboardButton("Finance", callback_data="cmd_finance"),
        InlineKeyboardButton("Contact", callback_data="cmd_contact"),
    ],
    [
        InlineKeyboardButton("Ping", callback_data="cmd_ping"),
    ],
]


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    PHOTO_URL = "https://i.pinimg.com/1200x/7a/1f/9b/7a1f9b0e7c59fda75644af099b092a17.jpg"
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=HELP_TEXT,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(BUTTONS),
    )


async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    # Импортируем тексты напрямую из хендлеров
    from handlers.about import about_command
    from handlers.project import project_command
    from handlers.shop import shop_command
    from handlers.finance import finance_command
    from handlers.contact import contact_command

    async def send(text, parse_mode="HTML"):
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)

    if query.data == "cmd_start":
        await send("<b>Welcome to Makki!</b>\n\nUse /help to see all commands.")

    elif query.data == "cmd_ping":
        await send("Pong! Bot is online.")

    elif query.data == "cmd_about":
        await about_command(_fake(chat_id, context), context)

    elif query.data == "cmd_project":
        await project_command(_fake(chat_id, context), context)

    elif query.data == "cmd_shop":
        await shop_command(_fake(chat_id, context), context)

    elif query.data == "cmd_finance":
        await finance_command(_fake(chat_id, context), context)

    elif query.data == "cmd_contact":
        await contact_command(_fake(chat_id, context), context)


def _fake(chat_id, context):
    """Минимальный fake update с правильным reply_text."""
    class FakeMessage:
        async def reply_text(self, text, parse_mode=None, **kwargs):
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                **kwargs
            )

    class FakeUpdate:
        message = FakeMessage()

    return FakeUpdate()


help_handler = CommandHandler("help", help_command)
help_button_handler = CallbackQueryHandler(help_button, pattern="^cmd_")