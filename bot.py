from dotenv import load_dotenv
load_dotenv()
import asyncio
import nest_asyncio
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)

from menus.main_menu import main_kb
from config import TELEGRAM_TOKEN
from storage.json_store import load_data, save_data
from handlers.core import start, handle_text
from handlers.add_coin import cb_add, cb_set_alert
from handlers.edit_coin import cb_edit_coin, cb_edit_main
from handlers.profile import show_profile
from services.price_watcher import watcher
from handlers.prices import show_prices


async def cb_all(update, ctx):
    q = update.callback_query
    data = q.data
    await q.answer()

    # 1. Вхід у меню редагування монети
    if data.startswith("edit_coin_"):
        return await cb_edit_coin(update, ctx)

    # 2. Повернення у список монет
    if data == "edit":
        return await cb_edit_main(update, ctx)

    # 3. Toggle та Remove
    if data.startswith("toggle_") or data.startswith("remove_"):
        return await cb_edit_main(update, ctx)

    # 4. Запит порогу через Change alert
    if data.startswith("change_alert_"):
        # наприклад: change_alert_BTC
        sym = data.split("_", 2)[-1]
        # знову показуємо клавіатуру вибору порогу
        from menus.add_menu import alert_kb
        return await q.edit_message_text(
            f"✅ {sym}: виберіть новий поріг:",
            reply_markup=alert_kb(sym)
        )

    # 5. Встановлення alert-порога
    if data.startswith("alert_"):
        return await cb_set_alert(update, ctx)

    # 6. Додавання
    if data.startswith("add_"):
        return await cb_add(update, ctx)

    # 7. Решта
    if data in ("add", "profile", "back_main", "prices", "main_menu"):
        if data == "add":
            return await cb_add(update, ctx)
        if data == "profile":
            uid = q.from_user.id
            from storage.json_store import user_data
            u = user_data.setdefault(uid, {"coins": {}, "wallets": {}, "nfts": {}})
            return await show_profile(q, u)
        if data in ("back_main", "main_menu"):
            return await q.edit_message_text("🔻 Main menu", reply_markup=main_kb())
        if data == "prices":
            return await show_prices(update, ctx)




async def main():
    load_data()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(cb_all))
    app.add_handler(CommandHandler("menu", lambda update, ctx: update.message.reply_text(
    "🔻 Main menu", reply_markup=main_kb()
)))

    print("Бот запущено!")

    async def run_watcher():
        while True:
            await watcher(app)
            await asyncio.sleep(500)

    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    loop.create_task(run_watcher())

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
