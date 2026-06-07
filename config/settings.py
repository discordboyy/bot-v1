# settings.py

import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# BOT CORE
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


# =========================
# BRAND (Makki)
# =========================

BRAND_NAME = "Makki"
BRAND_TAGLINE = "Process made visible"
BRAND_VERSION = "1.0"


# =========================
# ECONOMY SETTINGS (no DB yet)
# =========================

START_BALANCE = 0

DAILY_REWARD_AMOUNT = 100
DAILY_REWARD_COOLDOWN_DAYS = 1

FINANCE_MESSAGE_INTERVAL_DAYS = 3
SHOP_MESSAGE_INTERVAL_DAYS = 14


# =========================
# API KEYS (later)
# =========================

FRANKFURTER_API = "https://api.frankfurter.app"

BINANCE_API = "https://api.binance.com"


# =========================
# FEATURES FLAGS
# =========================

ENABLE_CASINO = False   # пока выключено (без DB)
ENABLE_SHOP = True
ENABLE_FINANCE = True


# =========================
# LIMITS
# =========================

MAX_WITHDRAW = 0  # пока нет экономики