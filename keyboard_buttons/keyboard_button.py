from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text= "✅",callback_data="True"), InlineKeyboardButton(text= "❌",callback_data="Folse")]
    ]
)