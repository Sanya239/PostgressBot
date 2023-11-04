import asyncio

import aiogram.utils.keyboard
from aiogram import Bot, Dispatcher, types, filters,Router

import Solutions

MyToken = "6671282083:AAFzQbNyUq3wbwRm8UWkcbPobFn1kyZ2RbE"
with open("users","r") as file:
    Admins = list(map(int,file.readlines()))


MyBot = Bot(MyToken)
dispatcher: Dispatcher = Dispatcher()
bb={}
bb["print"]=print
bb["print"](123)

@dispatcher.message(filters.Command(commands=["help"]))
async def help(message: types.Message):
    await MyBot.send_message(chat_id=message.from_user.id,text="list of commands:\n"
                                                               "/help to get help\n"
                                                               "/bind to bind\n"
                                                               "/start to start")
@dispatcher.message(filters.Command(commands=["key"]))
async def key(message: types.Message):
    #await Solutions.longSession(name="db1",users=Admins)
    await Solutions.solutions["long session"](name="db1",users=Admins)

@dispatcher.message(filters.Command(commands=["bind"]))
async def bind(message: types.Message):
    await MyBot.send_message(chat_id=message.from_user.id,text="Nothing to bind")


@dispatcher.message(filters.CommandStart())
async def say_hello(message: types.Message):
    if message.from_user.id not in Admins:
        Admins.append(message.from_user.id)
        with open("users","a") as file:
            file.write(str(message.from_user.id)+"\n")
        print(Admins)

    await MyBot.send_message(chat_id=message.from_user.id,text="welcome")
    await help(message=message)

@dispatcher.message(filters.Command(commands=["debug"]))
async def debug(message: types.Message):
    await MyBot.send_message(message.from_user.id,text="debug done")
    print(f"Admins={Admins}")


@dispatcher.message()
async def Respond(message: types.Message):
    await MyBot.send_message(chat_id=message.from_user.id, text="I'm still online)")


async def Alert(dbName: str, users: list[int]):
    for user_id in users:
        await MyBot.send_message(chat_id=user_id, text=f"Database {dbName} is broken")


async def poll():
    await dispatcher.start_polling(MyBot, polling_timeout=0)



