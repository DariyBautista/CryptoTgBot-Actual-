# core.py
from telegram import Update
from telegram.ext import ContextTypes
from menus.main_menu import main_kb
from menus.add_menu import alert_kb
import storage.json_store as json_store
from services.cmc import get_price_float
import re

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔻 Main menu", reply_markup=main_kb())

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # print("▶️ handle_text entered; await_coin:", ctx.user_data.get("await_coin"), "; user_data:", json_store.user_data)
    uid = update.message.from_user.id
    txt = update.message.text.strip().upper()
    u = json_store.user_data.setdefault(uid, {"coins": {}, "wallets": {}, "nfts": {}})
    text = update.message.text.strip().upper()
    # Якщо ми очікуємо, що зараз користувач надсилає символ монети
    if ctx.user_data.get("await_coin"):
        ctx.user_data["await_coin"] = False

        # Не додаємо дублікати
        if txt in u["coins"]:
            await update.message.reply_text(
                f"❗️ {txt} уже в обраних.",
                reply_markup=main_kb()
            )
            return

        # Додаємо монету
        u["coins"][txt] = {"track": None, "last": None}
        # print("📝 about to save; this user entry:", u)
        json_store.save_data()  # зберігаємо одразу після зміни
        # print("💾 after save; full user_data:", json_store.user_data)
        await update.message.reply_text(
            f"✅ {txt} added. Select alert threshold:",
            reply_markup=alert_kb(txt)
        )
        return
    
        # 2️⃣  Перевіряємо шаблон «<число> <символ>»
    m = re.fullmatch(r"\s*([\d.]+)\s+([a-zA-Z0-9]+)\s*", text)
    if m:
        qty, sym = float(m.group(1)), m.group(2).upper()
        price = await get_price_float(sym)
        if price is None:
            await update.message.reply_text(f"Не вдалося знайти ціну для {sym}.")
        else:
            total = qty * price
            await update.message.reply_text(
                f"{qty:g} {sym} ≈ **${total:,.2f}**",
                parse_mode="Markdown"
            )
        return

    # Усі інші тексти — просто показуємо головне меню
    await update.message.reply_text(
        "Choose from menu ↓",
        reply_markup=main_kb()
    )
