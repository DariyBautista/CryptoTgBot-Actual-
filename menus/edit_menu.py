from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def edit_menu_kb(coins: list[str]) -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(c, callback_data=f"edit_coin_{c}")] for c in coins]
    kb.append([InlineKeyboardButton("⬅️ Back", callback_data="back_main")])
    return InlineKeyboardMarkup(kb)

def coin_edit_kb(sym: str, tracking: int|None) -> InlineKeyboardMarkup:
    status = "Off" if tracking is None else "ON"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Toggle alert (now {status})", callback_data=f"toggle_{sym}")],
        [InlineKeyboardButton("Change alert", callback_data=f"change_alert_{sym}")],
        [InlineKeyboardButton("🗑 Remove",     callback_data=f"remove_{sym}")],
        [InlineKeyboardButton("⬅️ Back",       callback_data="edit")]
    ])
