from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Savat"), KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True,
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

language_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="🇺🇿 O‘zbekcha",
            callback_data="lang_uz"
        )],
        [InlineKeyboardButton(
            text="🇷🇺 Русский",
            callback_data="lang_ru"
        )]
    ]
)
