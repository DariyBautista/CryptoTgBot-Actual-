from telegram import Update
from menus.main_menu import main_kb

async def show_profile(q, u):
    txt = (f"👤 ID: {q.from_user.id}\n"
           f"• Coins:   {len(u.get('coins', []))}\n"
           f"• Wallets: {len(u.get('wallets', []))}\n"
           f"• NFTs:    {len(u.get('nfts', []))}")
    await q.edit_message_text(txt, reply_markup=main_kb())
