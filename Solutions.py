import bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, types, filters,Router
from aiogram import F

solutions = {}

async def longSession(name: str,users: list[int]):
    keyBoard = ReplyKeyboardBuilder()
    keyBoard.button(text="terminate session",callback_data="terminate")
    keyBoard.button(text="recheck status",callback_data="recheck")
    for user_id in users:
        await bot.MyBot.send_message(chat_id=user_id,text=f"options for {name}",reply_markup=keyBoard.as_markup(resize_keyboard=True))

@bot.dispatcher.message(F.text.lower()=="terminate session")
async def terminate(message: types.Message):
    await message.answer(text="imaginary session was terminated",reply_markup=types.ReplyKeyboardRemove())

@bot.dispatcher.message(F.text.lower()=="recheck status")
async def terminate(message: types.Message):
    await message.answer(text="still broken")

solutions["long session"]=longSession


