from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 

ads_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛎 E'lon berish")],
        [KeyboardButton(text="💁🏻‍♂️ Biz haqimizda"),KeyboardButton(text="📣 Kanal")]    
    ],
   resize_keyboard=True,
   input_field_placeholder="E'lon berish uchun bosing"
)