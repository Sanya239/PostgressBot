import builtins

import DataBasePeeker
import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, filters,Router
from aiogram import F
from aiogram.filters.callback_data import CallbackData,CallbackQuery
solutions = {}

class MyCallback(CallbackData,prefix = "terminate"):
    option_name:str
    db_id : int
    #func: callable = print      Not supported by pydantic whatever that means...


async def longSession(db: DataBasePeeker.DataBasePeeker, users: list[int]):
    keyBoard = InlineKeyboardBuilder()
    keyBoard.button(text="terminate session",callback_data=MyCallback(option_name="terminate",db_id = db.bid))
    keyBoard.button(text="recheck status",callback_data=MyCallback(option_name="recheck",db_id=db.bid))
    for user_id in users:
        await bot.MyBot.send_message(chat_id=user_id, text=f"options for {db.database}", reply_markup=keyBoard.as_markup(resize_keyboard=True))


@bot.dispatcher.callback_query(MyCallback.filter(F.option_name == "terminate"))
async def terminate(query: CallbackQuery, callback_data: MyCallback = None):
    id = MyCallback.unpack(query.data).db_id
    DataBasePeeker.DataBasePeeker.AllBases[id].fix(1)
    await query.message.answer(text="imaginary session was terminated",reply_markup=types.ReplyKeyboardRemove())
    await query.answer()


@bot.dispatcher.callback_query(MyCallback.filter(F.option_name == "recheck"))
async def terminate(query: CallbackQuery, callback_data: MyCallback = None):
    id = MyCallback.unpack(query.data).db_id
    state = DataBasePeeker.DataBasePeeker.AllBases[id].peek()
    if state=="ok":
        await query.message.answer(text="it's ok now",reply_markup=types.ReplyKeyboardRemove())
    else:
        await query.message.answer(text="still broken")
    await query.answer()


solutions["long session"]=longSession


