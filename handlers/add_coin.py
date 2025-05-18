from telegram import Update
from telegram.ext import ContextTypes
from menus.add_menu import add_kb, alert_kb
# from storage.json_store import user_data, save_data
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import storage.json_store as json_store
from services.cmc import get_price_float

async def cb_add(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "add":
        await q.edit_message_text("Select what to add:", reply_markup=add_kb())
        return

    uid = q.from_user.id
    u = json_store.user_data.setdefault(uid, {"coins": {}, "wallets": {}, "nfts": {}})

    if q.data == "add_coin":
        ctx.user_data["await_coin"] = True
        # print(f"✅ set await_coin for {q.from_user.id}")
        await q.edit_message_text("Send coin symbol (e.g., BTC)")
    elif q.data in ("add_wallet", "add_nft"):
        await q.edit_message_text("🚧 Feature in development.", reply_markup=add_kb())

async def cb_set_alert(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = json_store.user_data.setdefault(uid, {"coins": {}, "wallets": {}, "nfts": {}})
    parts = q.data.split('_')

    # Перевірка на коректність формату
    if len(parts) != 3:
        await q.edit_message_text("❌ Invalid alert data!")
        return

    _, coin, threshold = parts
    coin = coin.upper()
    
    if coin not in u["coins"]:
        # print(f"DEBUG: Coins in user_data: {list(u['coins'].keys())}")
        # print(f"DEBUG: Searched coin: {coin}")
        await q.edit_message_text("❌ Coin not found!")
        return

    cfg = u["coins"][coin]
    if threshold == "off":
        cfg["track"] = None
        text = f"🚫 Alert for {coin} turned off."
    else:
        try:
            val = float(threshold)
            cfg["track"] = val
            text = f"✅ Alert threshold for {coin} set to {val}%"
        except ValueError:
            await q.edit_message_text("❌ Invalid threshold value!")
            return
        
    current_price = await get_price_float(coin)
    if current_price is not None:
        cfg["last"] = current_price
        text += f"\n📝 Initialized baseline price: ${current_price:,.2f}"

    json_store.save_data()

    # Додаємо кнопку повернення на головне меню
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Повернутися на головне меню", callback_data="main_menu")]
    ])

    await q.edit_message_text(text, reply_markup=keyboard)