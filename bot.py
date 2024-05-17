from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message, CallbackQuery
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from filters.check_sub_channel import IsCheckSubChannels
from keyboard_buttons import admin_keyboard
from keyboard_buttons import keyboard_button
from aiogram.fsm.context import FSMContext
from states.sequence import Adverts, Info
import time 

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS
ADMINS_GROUP = config.ADMINS_GROUP

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz", reply_markup=admin_keyboard.ads_button)
    except:
        await message.answer(text="Assalomu alaykum", reply_markup=admin_keyboard.ads_button)

# Start
@dp.message(F.text == "🛎 E'lon berish")
async def info_to_ads(message:Message, state:FSMContext):

    await message.answer("Eslatma❗️ \nMa'lumotlarni to'g'ri kiriting❗️")
    await message.answer(text= "🖼 Telefongizni rasmini yuboting")
    await state.set_state(Info.pic)

# Pic
@dp.message(F.photo, Info.pic)
async def info_ads_pic(message:Message, state:FSMContext):
    pic = message.photo[-1].file_id
    await state.update_data(pic = pic)
    await message.answer("📱 Modelini kiriitng!")
    await state.set_state(Info.model)

@dp.message(Info.pic)
async def info_ads_pic_del(message:Message, state:FSMContext):
    await message.answer(text= "Rasmni yuboring!")
    await message.delete()

# Model
@dp.message(F.text, Info.model)
async def info_ads_model(message:Message, state:FSMContext):
    model = message.text
    await state.update_data(model = model)
    await message.answer("💾 Xotirani kiriitng!")
    await state.set_state(Info.memory)

@dp.message(Info.model)
async def info_ads_model_del(message:Message, state:FSMContext):
    await message.answer(text= "Modelini to'g'ri kiriitng!")
    await message.delete()

# Memory 
@dp.message(F.text, Info.memory)
async def info_ads_memory(message:Message, state:FSMContext):
    memory = message.text
    await state.update_data(memory = memory)
    await message.answer("📦 Karopka & 📑 dakumenti bormi!")
    await state.set_state(Info.document)

@dp.message(Info.memory)
async def info_ads_memory_del(message:Message, state:FSMContext):
    await message.answer(text= "Xotirani to'g'ri kiriitng!")
    await message.delete()

# Document + inline button
@dp.message(F.text, Info.document)
async def info_ads_document(message:Message, state:FSMContext):
    document = message.text
    await state.update_data(document = document)
    await message.answer("🎨 Telefon rangini kiriting!")
    await state.set_state(Info.color)

@dp.message(Info.document)
async def info_ads_documentdel(message:Message, state:FSMContext):
    await message.answer(text= "To'g'ri javob bering!")
    await message.delete()

# Color
@dp.message(F.text, Info.color)
async def info_ads_color(message:Message, state:FSMContext):
    color = message.text
    await state.update_data(color = color)
    await message.answer("🛠 Telefon usta ko'rganmi!")
    await state.set_state(Info.master)

@dp.message(Info.color)
async def info_ads_color_del(message:Message, state:FSMContext):
    await message.answer(text= "To'g'ri rang kiriting!")
    await message.delete()

# master
@dp.message(F.text, Info.master)
async def info_ads_master(message:Message, state:FSMContext):
    master = message.text
    await state.update_data(master = master)
    await message.answer("💵 Telefon narxini qancha qancha❗️")
    await state.set_state(Info.price)

@dp.message(Info.master)
async def info_ads_documentdel(message:Message, state:FSMContext):
    await message.answer(text= "To'g'ri javob bering!")
    await message.delete()

# xatolikni top
# @dp.message(F.text, Info.master)
# async def info_ads_master(message:Message, state:FSMContext):
#     master = message.text
#     await master.update_data(master = master)
#     await message.answer("💵 Telefon narxini qancha qancha❗️")
#     await state.set_state(Info.price)

# @dp.message(Info.master)
# async def info_ads_master_del(message:Message, state:FSMContext):
#     await message.answer(text= "Faqat to'g'risini ayting!")
#     await message.delete()

# price
@dp.message(F.text, Info.price)
async def info_ads_price(message:Message, state:FSMContext):
    price = message.text
    await state.update_data(price = price)
    await message.answer("☎️Telefon raqamingizni kiriting!")
    await state.set_state(Info.phone_number)

@dp.message(Info.price)
async def info_ads_price_del(message:Message, state:FSMContext):
    await message.answer(text= "Narxini to'g'ri kiriting!")
    await message.delete()

# phone_number
@dp.message(F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"), Info.phone_number)
async def info_ads_phone_number(message:Message, state:FSMContext):
    phone_number = message.text
    data = await state.get_data()
    pic = data.get("pic")
    model = data.get("model")
    memory = data.get("memory")
    document = data.get("document")
    color = data.get("color")
    master = data.get("master")
    price = data.get("price")
    text = f"#Sotilad \n📱 {model}\n💾 {memory} \n📦 & 📑 {document}\n🎨 {color}\n🛠 {master}\n💵 {price}\n☎️ {phone_number}"

    await bot.send_photo(chat_id=CHANNELS[0], photo=pic, caption=text, reply_markup=keyboard_button.confirmation)
    await message.answer("E'lonin giz adminga yuborildi! \nPulni to'lasangiz xabar Kanalga chiqadi!")
    await state.clear()

@dp.message(Info.phone_number)
async def info_ads_phone_number_del(message:Message):
    await message.answer(text= "Telefon raqamni to'g'ri kiriting!")
    await message.delete()
# Finish

@dp.callback_query(F.data=="False")
async def confirmation (callback_query: CallbackQuery):
    await callback_query.message.delete()
@dp.callback_query(F.data=="True")
async def confirmation (callback_query: CallbackQuery):
    rasm = callback_query.message.photo[-1].file_id
    text = callback_query.message.caption 
    await bot.send_photo(chat_id=ADMINS_GROUP[0], photo=rasm, caption=text)
    await callback_query.message.delete()


@dp.message(F.text == "💁🏻‍♂️ Biz haqimizda")
async def about_as(message:Message, ):

    await message.answer("Biz sizga telefoningizni sotishga yordam beramiz! \nSiz bot orqali telefoningizni ma'lumotlarini kiritasiz va bu ma'lumotlar adminga yuboriladi va ko'rib chiqadi! Agar admin ma'lumotni tasdiqlasa va siz e'lon uchun pulni to'lagan bo'lsangiz! E'loningiz kanalga qo'yiladi !")

@dp.message(F.text == "📣 Kanal")
async def chanals_link(message:Message):

    await message.answer("Bu bizning E'lonlarimiz chiqadigan kanal \nhttps://t.me/hrfhrrjryjryr")


#help commands
@dp.message(Command("help"))
async def help_commands(message:Message):
    await message.answer("Sizga qanday yordam kerak")


#about commands
@dp.message(Command("about"))
async def about_commands(message:Message):
    await message.answer("Bot sizga e'lon berishga yardam beradi!")


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


#bot ishga tushganini xabarini yuborish
@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))



async def main() -> None:
    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    await dp.start_polling(bot)
    setup_middlewares(dispatcher=dp, bot=bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())