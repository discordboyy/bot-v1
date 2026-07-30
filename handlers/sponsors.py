# handlers/sponsors.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki-v6.png"

# =========================
# SPONSORS / PARTNERS DATA
# =========================
# kind: "Sponsor" or "Partner" — just changes the label shown next to the name.
# Add/remove entries here whenever a new deal starts or ends, no other code needs to change.

SPONSORS = [
    {
        "name": "Marapain",
        "kind": "Partner",
        "description": "We are proud to partner with Marapain, supporting creative work and bringing more opportunities to our community.",
        "link": "https://t.me/marapainbeatssss",
    },
]


def build_sponsors_text() -> str:
    if not SPONSORS:
        return (
            "<b>Makki Sponsors & Partners 🦋</b>\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "No active sponsors or partners right now.\n"
            "Interested in partnering with Makki? Reach out via /contact."
        )

    lines = ["<b>Makki Sponsors & Partners 🦋</b>", "", "━━━━━━━━━━━━━━", ""]

    for s in SPONSORS:
        lines.append(f"<b>{s['name']}</b> — {s['kind']}")
        lines.append(s["description"])
        lines.append(f'<a href="{s["link"]}">{s["link"]}</a>')
        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    lines.append("")
    lines.append("Want to become a sponsor or partner? Use /contact.")
    lines.append("")
    lines.append('© 2025–2026 <a href="https://makki.no">Makki</a> — Growth • Creativity • Innovation')

    return "\n".join(lines)


def build_sponsors_keyboard() -> InlineKeyboardMarkup | None:
    if not SPONSORS:
        return None
    keyboard = [
        [InlineKeyboardButton(s["name"], url=s["link"])]
        for s in SPONSORS
    ]
    return InlineKeyboardMarkup(keyboard)


async def sponsors_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=PHOTO_URL,
        caption=build_sponsors_text(),
        parse_mode="HTML",
        reply_markup=build_sponsors_keyboard(),
    )


# Registered under two aliases so /sponsors and /partners both work.
sponsors_handler = CommandHandler(
    ["sponsors", "partners", "adv"],
    sponsors_command
)

async def send_sponsors_update(context):
    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=PHOTO_URL,
        caption=build_sponsors_text(),
        parse_mode="HTML",
        reply_markup=build_sponsors_keyboard(),
    )