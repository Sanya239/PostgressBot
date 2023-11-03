import asyncio

from aiogram import Bot, Dispatcher, types, filters

import DataBasePeeker

MyToken = "6671282083:AAFzQbNyUq3wbwRm8UWkcbPobFn1kyZ2RbE"
Admins = [856075248, 1395495575]

MyBot = Bot(MyToken)
dispatcher: Dispatcher = Dispatcher()

DataBase = DataBasePeeker.DataBasePeeker()


@dispatcher.message()
async def send_welcome(message: types.Message):
    if message.from_user.id not in Admins:
        Admins.append(message.from_user.id)
        print(Admins)
    await MyBot.send_message(chat_id=message.from_user.id, text="I'm still online)")


async def Alert(dbName: str, users: list[int]):
    for user_id in users:
        await MyBot.send_message(chat_id=user_id, text=f"Database {dbName} is broken")


async def poll():
    await dispatcher.start_polling(MyBot, polling_timeout=0)



