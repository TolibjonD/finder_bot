from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

startBtn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Qidiruv...")
        ],
        [
            KeyboardButton(text="Sport mahsulotlari ⛹🏼‍♂️")
        ],
    ],
    resize_keyboard=True
)

productsBtn=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Gainerlar - Massa olish")], 
        [KeyboardButton(text="Protainlar")], 
        [KeyboardButton(text="Kreatinlar")], 
        [KeyboardButton(text="🔙 Bosh sahifa")], 
    ],
    resize_keyboard=True
)