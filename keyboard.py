from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu = [
    [
        InlineKeyboardButton(text="⛅️ Погода", callback_data="weather"),
        InlineKeyboardButton(text="💰 Курс валют", callback_data="exchange"),
    ],
    [
        InlineKeyboardButton(text="📝 Чат з OpenAI", callback_data="generate_text"),
        InlineKeyboardButton(text="🖼 Генерувати фото", callback_data="generate_image"),
    ],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Вийти в меню")]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Вийти в меню", callback_data="menu")]
    ]
)
