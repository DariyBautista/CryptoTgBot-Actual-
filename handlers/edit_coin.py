from telegram import Update
from telegram.ext import ContextTypes
from storage.json_store import user_data, save_data
import storage.json_store as json_store
from menus.edit_menu import edit_menu_kb, coin_edit_kb
from menus.main_menu import main_kb
from menus.add_menu import alert_kb
async def show_edit_menu(q, u):
    coins = list(u["coins"])
    if not coins:
        await q.edit_message_text("No coins added.", reply_markup=main_kb())
        return
    kb = edit_menu_kb(coins)
    await q.edit_message_text("🔧 Select asset to edit:", reply_markup=kb)

async def cb_edit_coin(update: Update, _):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    sym = q.data.split("_")[-1]
    cfg = json_store.user_data[uid]["coins"][sym]
    kb = coin_edit_kb(sym, cfg["track"])
    await q.edit_message_text(f"⚙️ {sym} settings:", reply_markup=kb)

async def cb_edit_main(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = json_store.user_data.setdefault(uid, {"coins": {}, "wallets": {}, "nfts": {}})
    data = q.data

    if data == "edit":
        return await show_edit_menu(q, u)

    # розбираємо sym
    prefix, sym = data.split("_", 1)

    if prefix == "toggle":
        cfg = u["coins"][sym]
        cfg["track"] = None if cfg["track"] else 10
        json_store.save_data()
        status = "Off" if cfg["track"] is None else "ON"
        return await q.edit_message_text(f"{sym}: alert {status}", reply_markup=main_kb())

    if prefix == "remove":
        u["coins"].pop(sym, None)
        json_store.save_data()
        return await q.edit_message_text(f"🗑 {sym} removed.", reply_markup=main_kb())

    if prefix == "change":
        # показуємо існуючі варіанти від alert_kb
        return await q.edit_message_text(
            f"🔃 Change alert for {sym}:",
            reply_markup=alert_kb(sym)
        )
