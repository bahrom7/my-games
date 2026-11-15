from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import MENU


inlineKy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🍽 Menyu", callback_data="menu")],
    [InlineKeyboardButton(text="📍 Filiallar", callback_data="branches")],
    [InlineKeyboardButton(text="🔗 Linklar", callback_data="links")],
])


back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")],
])

links_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/lazzat")],
    [InlineKeyboardButton(text="✈️ Telegram kanal", url="https://t.me/lazzat")],
    [InlineKeyboardButton(text="🌐 Sayt", url="https://evos.uz")],
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")],
])


cart_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="order")],
    [InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data="clear")],
])


def menu_kb() -> InlineKeyboardMarkup:
    """Menyudagi har bir taom uchun tugma (bosilsa savatga qo'shiladi)."""
    rows = []
    for item_id, item in MENU.items():
        rows.append([
            InlineKeyboardButton(
                text=f"{item['name']} — {item['price']:,} so'm".replace(",", " "),
                callback_data=f"add:{item_id}",
            )
        ])
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


