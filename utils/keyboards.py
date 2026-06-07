from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================
# MAIN MENU
# =========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Finance", callback_data="finance")],
        [InlineKeyboardButton("🛒 Shop", callback_data="shop")],
        [InlineKeyboardButton("🎮 Casino", callback_data="casino")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📞 Contact", callback_data="contact")]
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# FINANCE MENU
# =========================

def finance_menu():
    keyboard = [
        [InlineKeyboardButton("💱 Forex", callback_data="fx")],
        [InlineKeyboardButton("🪙 Crypto", callback_data="crypto")],
        [InlineKeyboardButton("📊 Rates", callback_data="rates")]
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# SHOP MENU
# =========================

def shop_menu():
    keyboard = [
        [InlineKeyboardButton("🎨 Landing Site (10k NOK)", callback_data="shop_landing")],
        [InlineKeyboardButton("🚀 MVP (30k NOK)", callback_data="shop_mvp")],
        [InlineKeyboardButton("💻 Web App (50k NOK)", callback_data="shop_webapp")],
        [InlineKeyboardButton("✍️ Autograph (100$)", callback_data="shop_autograph")],
        [InlineKeyboardButton("🎮 Discord Nitro (10k pts)", callback_data="shop_nitro")]
    ]
    return InlineKeyboardMarkup(keyboard)