import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from reply_keyboard import language_kb
from data import MENU, BRANCHES, PHONE
from inline_keyboard import inlineKy, back_kb, links_kb, cart_kb, menu_kb
from reply_keyboard import main_reply_kb

BOT_TOKEN = "Your token from bot father"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


carts: dict[int, dict[str, int]] = {}


def fmt(price: int) -> str:
    return f"{price:,}".replace(",", " ")


def cart_text(user_id: int) -> str | None:
    cart = carts.get(user_id)
    if not cart:
        return None
    lines = ["🛒 <b>Sizning savatingiz:</b>\n"]
    total = 0
    for item_id, qty in cart.items():
        item = MENU[item_id]
        summa = item["price"] * qty
        total += summa
        lines.append(f"{item['name']} × {qty} = {fmt(summa)} so'm")
    lines.append(f"\n💰 <b>Jami: {fmt(total)} so'm</b>")
    return "\n".join(lines)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Lazzat restoraniga xush kelibsiz! 👋\n"
        "Pastdagi <b>🛒 Savat</b> tugmasi orqali buyurtmangizni ko'rishingiz mumkin.",
        reply_markup=main_reply_kb,
        parse_mode="HTML",
    )
    await message.answer("Bo'limni tanlang:", reply_markup=inlineKy)

@dp.message(Command("about"))
async def start_handler(message: Message):
    await message.answer(
    """Lazzat restauranti navoiy viloyatidagi yangi restaurant!!
    U restaurant 2025 yilda ko'plab mijozlarga ega va hozirda u yerda katta tajribali cheflar bor!!!
    Siz u yerdan milliy taomlar, chet el va fast food taomlarini buyurtma qilish imkoniga egasiz!!""",
        reply_markup=main_reply_kb,
        parse_mode="HTML",
    )

@dp.message(Command("settings"))
async def start_handler(message: Message):
    await message.answer("Sozlamalar", reply_markup=main_reply_kb, parse_mode="HTML")

@dp.message(Command("deletechat"))
async def start_handler(message: Message):
    await message.answer("Chatni o'chrmoqchi bo'lsangiz unda tepadan delete chat tugmasini bosing", reply_markup=main_reply_kb, parse_mode="HTML")
    
@dp.message(F.text == "⚙️ Sozlamalar")
async def settings(message: Message):
    await message.answer("Tilni tanlang: 🇷🇺/🇺🇿",
        reply_markup=language_kb,
    )
    
    
@dp.message(F.text == "🛒 Savat")
async def show_cart(message: Message):
    text = cart_text(message.from_user.id)
    if text is None:
        await message.answer("Savatingiz hozircha bo'sh 🛒\nMenyudan taom tanlang.", reply_markup=inlineKy)
        return
    await message.answer(text, reply_markup=cart_kb, parse_mode="HTML")


@dp.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🍽 <b>Menyu</b>\nTaomni bosing — savatga qo'shiladi:",
        reply_markup=menu_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("add:"))
async def add_to_cart(callback: CallbackQuery):
    item_id = callback.data.split(":")[1]
    if item_id not in MENU:
        await callback.answer("Bunday taom topilmadi", show_alert=True)
        return
    cart = carts.setdefault(callback.from_user.id, {})
    cart[item_id] = cart.get(item_id, 0) + 1
    await callback.answer(f"{MENU[item_id]['name']} savatga qo'shildi ✅ (jami: {cart[item_id]})")


@dp.callback_query(F.data == "branches")
async def show_branches(callback: CallbackQuery):
    text = "📍 <b>Filiallarimiz:</b>\n\n" + "\n\n".join(BRANCHES) + f"\n\n📞 Aloqa: {PHONE}"
    await callback.message.edit_text(text, reply_markup=back_kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "links")
async def show_links(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔗 <b>Bizning sahifalarimiz:</b>",
        reply_markup=links_kb,
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text("Bo'limni tanlang:", reply_markup=inlineKy)
    await callback.answer()


@dp.callback_query(F.data == "clear")
async def clear_cart(callback: CallbackQuery):
    carts.pop(callback.from_user.id, None)
    await callback.message.edit_text("Savat tozalandi 🗑")
    await callback.answer()


@dp.callback_query(F.data == "order")
async def make_order(callback: CallbackQuery):
    text = cart_text(callback.from_user.id)
    if text is None:
        await callback.answer("Savat bo'sh", show_alert=True)
        return
    carts.pop(callback.from_user.id, None)
    await callback.message.edit_text(
        text + f"\n\n✅ Buyurtmangiz qabul qilindi! Tez orada {PHONE} dan bog'lanamiz.",
        parse_mode="HTML",
    )
    await callback.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
