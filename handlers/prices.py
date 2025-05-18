from telegram import Update
from telegram.ext import ContextTypes
# from storage.json_store import user_data
import storage.json_store as json_store
from menus.main_menu import main_kb
import asyncio
from services.cmc import get_price_float  # Імпортуємо функцію для отримання ціни з CMC

async def show_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = json_store.user_data.setdefault(uid, {"coins": {}, "wallets": {}, "nfts": {}})

    if not u["coins"]:
        await q.edit_message_text("У вас ще немає доданих монет.", reply_markup=main_kb())
        return

    prices_text = "💰 Поточні ціни ваших монет:\n\n"
    tasks = [get_price_float(coin) for coin in u["coins"]]  # Використовуємо get_price_float з cmc.py
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for coin, price in zip(u["coins"], results):
        if isinstance(price, Exception):
            prices_text += f"{coin}: помилка отримання ціни\n"
        elif price is not None:
            prices_text += f"{coin}: ${price:.2f}\n"
        else:
            prices_text += f"{coin}: ціна недоступна\n"

    await q.edit_message_text(prices_text, reply_markup=main_kb())
