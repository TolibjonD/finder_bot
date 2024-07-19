from aiogram import Bot, Dispatcher, types
from environs import Env
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
from sys import stdout
import logging
from aiogram.filters import CommandStart, Command, StateFilter
from keyboards.inline.simple import simple, simple_two, MyCallback
from aiogram.types.callback_query import CallbackQuery
from aiogram import F
from time import sleep
from keyboards.default.startBtn import startBtn
from states import SearchingState, ItemsState
from aiogram.fsm.context import FSMContext
from finder import search
from aiogram.enums.content_type import ContentType

from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION, KICKED
from aiogram.types import ChatMemberUpdated

env = Env()
env.read_env()
BOT_TOKEN=env('BOT_TOKEN')
ADMIN=5944280734
GROUP=-4227023516


dp = Dispatcher()

@dp.message(Command('help'))
async def help(msg: types.Message, bot: Bot):
    text = f"/help buyrug'i {msg.from_user.mention_html(msg.from_user.full_name)} tomonidan ishlatildi."
    await bot.send_message(chat_id=ADMIN, text=text)
    await msg.answer("Qidiruv tugmasini bosing va botga qidirmoqchi bo'lgan textingizni yuboring. Agar xatolilar kuzatilsa @Saidkodirov ga yozing.")

@dp.message(StateFilter(SearchingState.query))
async def simple_handler(msg: types.Message, bot: Bot, state: FSMContext):
    text = msg.text
    text_admin = f"{text} - {msg.from_user.mention_html(msg.from_user.full_name)} tomonidan yuborildi."
    await bot.send_message(chat_id=ADMIN, text=text_admin)
    data = await search(text)
    if type(data) == str:
        await msg.answer(text=data)
        await bot.send_message(chat_id=ADMIN, text=f"{data} - {msg.from_user.mention_html(msg.from_user.full_name)}")
        await state.clear()
    else:
        ans_text = f"🔎 Qidiriv natijangiz bo'yicha {len(data)} ta ma'lumot topildi"
        await msg.answer(text=ans_text, reply_markup=simple)
        await state.update_data({
            "query": data
        })
        await bot.send_message(chat_id=GROUP, text=f"{msg.from_user.mention_html(msg.from_user.full_name)}:\n\n")
        for item in data:
            for key,value in item.items():
                sleep(5)
                await bot.send_message(chat_id=GROUP, text=f"{key}: {value}")


@dp.callback_query(MyCallback.filter(F.item=="Simple"))
async def change_keyboard(call: CallbackQuery,bot: Bot, state: FSMContext):

    data = await state.get_data()
    data = data['query']
    await state.clear()
    await state.set_state(ItemsState.items)
    await state.update_data(
        {"items": data}
    )
    await state.set_state(ItemsState.index)
    await state.update_data(
        {"index": 0}
    )
    first_item = data[0]
    title = first_item['title']
    snippet = first_item['snippet']
    link = first_item['link']
    photo = first_item['image']
    await call.answer(cache_time=60)
    await call.message.delete()
    sleep(1)
    text = f"{title}\n"
    text += f"<blockquote>{snippet}</blockquote>\n"
    text += f"\n<a href='{link}'>Batafsil...</a>\n\n"
    text += f"{link}"
    if photo:
        photo=photo
    else:
        photo = "https://1.bp.blogspot.com/-BXV4NsmA43Y/WLf4BZwJiOI/AAAAAAAATU8/rEKAYq7bb8c1BjXagUD3FpHN_yX53X36QCLcB/s1600/thumbnail.gif"

    try:
        await call.message.answer_photo(photo=photo, caption=text, reply_markup=simple_two)
        await bot.send_message(chat_id=ADMIN, text=f"{call.from_user.mention_html(call.from_user.full_name)}:\n\n")
        await bot.send_photo(chat_id=ADMIN, photo=photo, caption=text)
    except:
        await call.message.answer("Ma'lumot yoq yoki ma'lumot manbasi o'zgargan", reply_markup=simple_two)
        await bot.send_message(chat_id=ADMIN, text=f"{call.from_user.mention_html(call.from_user.full_name)}:\n\n")
    await call.answer(cache_time=60)

@dp.callback_query(MyCallback.filter(F.item=="prev"))
async def previous_item(call: CallbackQuery,bot: Bot, state: FSMContext):
    data = await state.get_data()
    items = data['items']
    index = data['index']
    if index>0:
        index=index-1
    else:
        index=0
    await state.set_state(ItemsState.items)
    await state.update_data(
        {"items": items}
    )
    await state.set_state(ItemsState.index)
    await state.update_data(
        {"index": index}
    )
    first_item = items[index]
    title = first_item['title']
    snippet = first_item['snippet']
    link = first_item['link']
    photo = first_item['image']
    await call.answer(cache_time=60)
    await call.message.delete()
    sleep(1)
    text = f"{index+1}-natija {len(items)} dan.\n"
    text += f"{title}\n"
    text += f"<blockquote>{snippet}</blockquote>\n"
    text += f"\n<a href='{link}'>Batafsil...</a>\n\n"
    text += f"{link}"
    if photo:
        photo=photo
    else:
        photo = "https://www.kancbag.ru/_img/cmall/icon__CmallEmptyBigImg.png"

    try:
        await call.message.answer_photo(photo=photo, caption=text, reply_markup=simple_two)
        await bot.send_photo(chat_id=ADMIN, photo=photo, caption=text)
    except:
        await call.message.answer("Ma'lumot yoq yoki ma'lumot manbasi o'zgargan", reply_markup=simple_two)
    await call.answer(cache_time=60)

@dp.callback_query(MyCallback.filter(F.item=="next"))
async def next_item(call: CallbackQuery,bot: Bot, state: FSMContext):
    data = await state.get_data()
    items = data['items']
    index = data['index']
    if index>=0 and index<len(items):
        index=index+1
    else:
        index=len(items)-1
    await state.set_state(ItemsState.items)
    await state.update_data(
        {"items": items}
    )
    await state.set_state(ItemsState.index)
    await state.update_data(
        {"index": index}
    )
    first_item = items[index]
    title = first_item['title']
    snippet = first_item['snippet']
    link = first_item['link']
    photo = first_item['image']
    await call.answer(cache_time=60)
    await call.message.delete()
    sleep(1)
    text = f"{index+1}-Natija.\n"
    text += f"{title}\n"
    text += f"<blockquote>{snippet}</blockquote>\n"
    text += f"\n<a href='{link}'>Batafsil...</a>\n\n"
    text += f"{link}"
    if photo:
        photo=photo
    else:
        photo = "https://smart.mag-river.ru/uploads/goods/img/445-360/fit/no-image.png"

    try:
        await call.message.answer_photo(photo=photo, caption=text, reply_markup=simple_two)
        await bot.send_photo(chat_id=ADMIN, photo=photo, caption=text)
    except:
        await call.message.answer("Ma'lumot yoq yoki ma'lumot manbasi o'zgargan", reply_markup=simple_two)
    await call.answer(cache_time=60)

@dp.callback_query(MyCallback.filter(F.item=="cancel"))
async def calcel_simple(call: CallbackQuery,bot: Bot, state: FSMContext):
    await state.clear()
    await call.answer("Siz qidiruv natijalarini yopdingiz !", show_alert=True)
    await bot.send_message(chat_id=ADMIN, text=f"Cancel ishlatildi - {call.from_user.mention_html(call.from_user.full_name)}")
    await call.message.delete()

@dp.message(CommandStart())
async def start_bot(msg: types.Message, bot: Bot):
    await bot.send_message(chat_id=ADMIN, text=f"Bot ishlatildi - {msg.from_user.mention_html(msg.from_user.full_name)}")
    await msg.answer(f"Hush kelibsiz {msg.from_user.full_name}\nPastdagi tugmani bosish orqali qidiruvlarni amalga oshiring.", reply_markup=startBtn)

@dp.message(F.text=="Qidiruv...")
async def searching(msg: types.Message,bot: Bot, state: FSMContext):
    await msg.answer("Nimani izlamoqchi bo'lsangiz yozing, Marhamat: ")
    await bot.send_message(chat_id=ADMIN, text=f"Qidiruv knopkasi bosildi - {msg.from_user.mention_html(msg.from_user.full_name)}")
    await state.set_state(SearchingState.query)



@dp.message()
async def echo_handler(message: types.Message, bot: Bot) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        print(message)
        # Send a copy of the received message
        await message.answer("Qidiruvni boshlash uchun pastdan tugmani bosing.")
        await bot.send_message(chat_id=ADMIN, text=f"{message.text} - {message.from_user.mention_html(message.from_user.full_name)}")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=stdout)
    asyncio.run(main())