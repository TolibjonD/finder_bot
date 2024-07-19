from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix="simple"):
    item: str
    index: int

simple = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👁‍🗨 Ma'lumotlarni ko'rishni boshlash",
                                 callback_data=MyCallback(item="Simple", index="1").pack()
                                 )
        ],
        [
            InlineKeyboardButton(text="🔙 Qidiruvni tugallash",
                                 callback_data=MyCallback(item="cancel", index="0").pack()
                                 )
        ]
    ]
)
simple_two = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⏮", callback_data=MyCallback(item="prev", index="2").pack()),
            InlineKeyboardButton(text="⏭", callback_data=MyCallback(item="next", index="2").pack()),
            ],
             [
            InlineKeyboardButton(text="🔙 Ortga qaytish",
                                 callback_data=MyCallback(item="cancel", index="0").pack()
                                 )
        ]
    ]
)