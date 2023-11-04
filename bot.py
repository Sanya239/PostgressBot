import asyncio

import aiogram.utils.keyboard
from aiogram import Bot, Dispatcher, types, filters, Router

import DataBasePeeker

MyToken = "6671282083:AAFzQbNyUq3wbwRm8UWkcbPobFn1kyZ2RbE"
with open("users", "r") as file:
    Admins = list(map(int, file.readlines()))

MyBot = Bot(MyToken)
dispatcher: Dispatcher = Dispatcher()
DataBases: dict[DataBasePeeker.DataBasePeeker, list[int]] = {}

import Solutions
@dispatcher.message(filters.Command(commands=["help"]))
async def help(message: types.Message):
    await MyBot.send_message(chat_id=message.from_user.id, text="list of commands:\n"
                                                                "/help to get help\n"
                                                                "/bind to bind\n"
                                                                "/start to start")

db_test = DataBasePeeker.DataBasePeeker(1,2,3,4)
DataBases[db_test] = Admins
@dispatcher.message(filters.Command(commands=["error"]))
async def key(message: types.Message):
    # await Solutions.longSession(name="db1",users=Admins)
    await Solutions.solutions["long session"](db=db_test, users=Admins)


@dispatcher.message(filters.Command(commands=["bind"]))
async def bind(message: types.Message):
    bi, database, host, user, password = [None]*5
    try:
        bi,database, host, user, password = message.text.split("\n")
    except:
        await MyBot.send_message(chat_id=message.from_user.id, text="Incorrect input for command bind")
        pass
    for bd in DataBases.keys():
        if bd.database == database:
            DataBases[bd].append(message.from_user.id)
            await MyBot.send_message(chat_id=message.from_user.id, text="bind succeed")
            pass
    #TODO тут надо сделать чтобы не падало на некорректных данных
    new_db = DataBasePeeker.DataBasePeeker(database, host, user, password)
    if new_db.valid:
        DataBases[new_db] = [message.from_user.id]
        await MyBot.send_message(chat_id=message.from_user.id, text="bind succeed")
    else:
        await MyBot.send_message(chat_id=message.from_user.id, text="Database not found")



@dispatcher.message(filters.CommandStart())
async def say_hello(message: types.Message):
    if message.from_user.id not in Admins:
        Admins.append(message.from_user.id)
        with open("users", "a") as file:
            file.write(str(message.from_user.id) + "\n")
        print(Admins)

    await MyBot.send_message(chat_id=message.from_user.id, text="welcome")
    await help(message=message)


@dispatcher.message(filters.Command(commands=["debug"]))
async def debug(message: types.Message):
    await MyBot.send_message(message.from_user.id, text="debug done")
    print(f"Admins={Admins}")


@dispatcher.message()
async def Respond(message: types.Message):
    await MyBot.send_message(chat_id=message.from_user.id, text="I'm still online)")


async def Alert(dbName: str, users: list[int]):
    for user_id in users:
        await MyBot.send_message(chat_id=user_id, text=f"Database {dbName} is broken")


async def poll():
    await dispatcher.start_polling(MyBot, polling_timeout=0)
