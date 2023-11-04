import asyncio
import DataBasePeeker
import bot
import Solutions



async def CheckBases():
    while True:
        for db in bot.DataBases.keys():
            state = db.peek()
            #TODO тут проверить что с базой всё ок. Если не ок, то вызвать из Solutions.solutions функцию с названием как у ошибки.
            #пока есть только для названия ошибки "long session"
            if state == "ok":
                print("Error")
                await bot.Alert(dbName=db.database, users=bot.DataBases[db])
                await Solutions.solutions[state](db=db,users=bot.DataBases[db])
        await asyncio.sleep(10)


async def main():
    await asyncio.create_task(bot.poll())
    await asyncio.create_task(CheckBases())


if __name__ == "__main__":
    asyncio.run(main())
    print(239)

