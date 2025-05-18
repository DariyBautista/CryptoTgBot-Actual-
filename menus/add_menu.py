from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def add_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Coin", callback_data="add_coin")],
        [InlineKeyboardButton("Wallet", callback_data="add_wallet")],
        [InlineKeyboardButton("NFT", callback_data="add_nft")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
    ])

def alert_kb(sym: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("5 %", callback_data=f"alert_{sym}_5"),
            InlineKeyboardButton("10 %", callback_data=f"alert_{sym}_10"),
            InlineKeyboardButton("25 %", callback_data=f"alert_{sym}_25")
        ],
        [InlineKeyboardButton("🚫 Off", callback_data=f"alert_{sym}_off")]
    ])
