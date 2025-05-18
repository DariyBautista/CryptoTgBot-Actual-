from storage.json_store import user_data, save_data
import storage.json_store as json_store
from services.cmc import get_price_float

async def watcher(ctx):
    for uid, u in json_store.user_data.items():
        for sym, cfg in u["coins"].items():
            trig = cfg.get("track")
            if not trig:
                continue

            try:
                p = await get_price_float(sym)
                if p is None:
                    continue

                last = cfg.get("last")
                # 1) Іниціалізація
                if last is None:
                    cfg["last"] = p
                    # print(f"[{sym}] Init last price for user {uid}: {p}")
                    continue

                # 2) Розрахунок відсоткової зміни
                diff = (p - last) / last * 100
                # print(f"[{sym}] User {uid} price: {p:.4f}, last: {last:.4f}, diff: {diff:.2f}%")

                # 3) Якщо перевищує поріг — відправляємо алерт і тільки після цього оновлюємо last
                if abs(diff) >= trig:
                    sign = "📈" if diff > 0 else "📉"
                    txt = f"{sign} {sym} {diff:+.2f}%\nNew: ${p:,.2f}"
                    try:
                        await ctx.bot.send_message(uid, txt)
                        # print(f"Sent alert to {uid} for {sym}: {txt}")
                    except Exception as e:
                        print(f"Failed to send message to {uid}: {e}")
                    # Оновлюємо baseline тільки після алерту
                    cfg["last"] = p

            except Exception as e:
                print(f"Error fetching price for {sym}: {e}")

    json_store.save_data()
