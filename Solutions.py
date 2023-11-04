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
    #TODO эта функция создаё варианты что сделать когда сломалась база.
    #Если нужны ещё варианты, помимо имеющихся то создаё их как ниже. Нужно только моменять названия ниже
    #keyBoard.button(text="button_name",callback_data=MyCallback(option_name="option1",db_id = db.bid))
    keyBoard.button(text="terminate session",callback_data=MyCallback(option_name="terminate",db_id = db.bid))
    keyBoard.button(text="recheck status",callback_data=MyCallback(option_name="recheck",db_id=db.bid))
    for user_id in users:
        await bot.MyBot.send_message(chat_id=user_id, text=f"options for {db.database}", reply_markup=keyBoard.as_markup(resize_keyboard=True))

#TODO это обработчик нажатия кнопки.  Если добавишь новые кнопки как в шаблоне ниже, то он понадобится
"""
@bot.dispatcher.callback_query(MyCallback.filter(F.option_name == "option1"))
async def terminate(query: CallbackQuery, callback_data: MyCallback = None):
    id = MyCallback.unpack(query.data).db_id
    DataBasePeeker.DataBasePeeker.AllBases[id].yourMethod()
    await query.message.answer(text="your message", reply_markup=types.ReplyKeyboardRemove() <- если кнопки надо оставить, сотри этот аргумент)
    await query.answer()
"""

@bot.dispatcher.callback_query(MyCallback.filter(F.option_name == "terminate"))
async def terminate(query: CallbackQuery, callback_data: MyCallback = None):
    id = MyCallback.unpack(query.data).db_id
    # TODO сюда прифигачить починку вместо fix. В списке All Bases хранятся все базы, а AllBases[id] эта та, которую надо чинаить отрубив соединение.
    # перед починкой проверь ещё раз, что база сломана
    print()
    DataBasePeeker.DataBasePeeker.AllBases[id].fix(1)
    await query.message.answer(text="imaginary session was terminated",reply_markup=types.ReplyKeyboardRemove())
    await query.answer()


@bot.dispatcher.callback_query(MyCallback.filter(F.option_name == "recheck"))
async def terminate(query: CallbackQuery, callback_data: MyCallback = None):
    id = MyCallback.unpack(query.data).db_id
    #TODO тут надо прочекать что всё в порядке (поправь только условие)
    state = DataBasePeeker.DataBasePeeker.AllBases[id].peek()
    if state=="ok":
        await query.message.answer(text="it's ok now",reply_markup=types.ReplyKeyboardRemove())
    else:
        await query.message.answer(text="still broken")
    await query.answer()



#TODO это словарь доступных фиксов. Пока тут всего один.
solutions["long session"]=longSession


