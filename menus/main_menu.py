from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add", callback_data="add")],
        [InlineKeyboardButton("✏️ Edit", callback_data="edit")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("📈 Prices", callback_data="prices")]
    ])
