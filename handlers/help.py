from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

HELP_TEXT = """🌑 <b>Makki — Command Center</b>

━━━━━━━━━━━━━━

Choose a section below or type any command directly."""

BUTTONS = [
    [
        InlineKeyboardButton("🏠 Start", callback_data="cmd_start"),
        InlineKeyboardButton("🌍 About", callback_data="cmd_about"),
    ],
    [
        InlineKeyboardButton("🚀 Project", callback_data="cmd_project"),
        InlineKeyboardButton("🛍 Shop", callback_data="cmd_shop"),
    ],
    [
        InlineKeyboardButton("💹 Finance", callback_data="cmd_finance"),
        InlineKeyboardButton("📩 Contact", callback_data="cmd_contact"),
    ],
    [
        InlineKeyboardButton("🏓 Ping", callback_data="cmd_ping"),
    ],
]


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Когда будет фото — раскомментируй блок с photo и удали reply_text
    # PHOTO_URL = "https://your-image-url.jpg"
    # await update.message.reply_photo(
    #     photo=PHOTO_URL,
    #     caption=HELP_TEXT,
    #     parse_mode="HTML",
    #     reply_markup=InlineKeyboardMarkup(BUTTONS),
    # )
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(BUTTONS),
    )


async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    commands = {
        "cmd_start":   ("start",   "👋 Welcome to Makki!\n\nUse the buttons below to explore."),
        "cmd_about":   ("about",   None),
        "cmd_project": ("project", None),
        "cmd_shop":    ("shop",    None),
        "cmd_finance": ("finance", None),
        "cmd_contact": ("contact", None),
        "cmd_ping":    ("ping",    "🏓 Pong! Bot is online."),
    }

    data = query.data
    if data not in commands:
        return

    cmd_name, fallback = commands[data]

    # Ищем хендлер по имени команды и вызываем его напрямую
    from handlers.about import about_command
    from handlers.project import project_command
    from handlers.shop import shop_command
    from handlers.finance import finance_command
    from handlers.contact import contact_command

    handler_map = {
        "about":   about_command,
        "project": project_command,
        "shop":    shop_command,
        "finance": finance_command,
        "contact": contact_command,
    }

    if cmd_name in handler_map:
        # Подменяем update так чтобы хендлер отвечал в тот же чат
        class FakeUpdate:
            class FakeMessage:
                chat_id = query.message.chat_id
                async def reply_text(self, *args, **kwargs):
                    await context.bot.send_message(
                        chat_id=query.message.chat_id, *args, **kwargs
                    )
            message = FakeMessage()

        await handler_map[cmd_name](FakeUpdate(), context)
    else:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=fallback,
        )


help_handler = CommandHandler("help", help_command)
help_button_handler = CallbackQueryHandler(help_button, pattern="^cmd_")