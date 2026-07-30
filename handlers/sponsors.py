# handlers/sponsors.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

PHOTO_URL = "https://raw.githubusercontent.com/discordboyy/bot-v1/main/assets/makki-v3.png"

# =========================
# SPONSORS / PARTNERS DATA
# =========================
# kind: "Sponsor" or "Partner" — just changes the label shown next to the name.
# Add/remove entries here whenever a new deal starts or ends, no other code needs to change.

SPONSORS = [
    {
        "name": "Example Sponsor",
        "kind": "Sponsor",
        "description": "Short one-line pitch of what they do and why it matters to our audience.",
        "link": "https://example.com",
    },
    {
        "name": "Example Partner",
        "kind": "Partner",
        "description": "Short one-line pitch of the partnership / what users get from them.",
        "link": "https://example.com",
    },
]


def _kind_emoji(kind: str) -> str:
    return "💎" if kind.lower() == "sponsor" else "🤝"


def build_sponsors_text() -> str:
    if not SPONSORS:
        return (
            "<b>Makki Sponsors & Partners 🤝</b>\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "No active sponsors or partners right now.\n"
            "Interested in partnering with Makki? Reach out via /contact."
        )

    lines = ["<b>Makki Sponsors & Partners 🤝</b>", "", "━━━━━━━━━━━━━━", ""]

    for s in SPONSORS:
        emoji = _kind_emoji(s["kind"])
        lines.append(f"{emoji} <b>{s['name']}</b> — {s['kind']}")
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
        [InlineKeyboardButton(f"{_kind_emoji(s['kind'])} {s['name']}", url=s["link"])]
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
sponsors_handler = CommandHandler(["sponsors", "partners"], sponsors_command)
