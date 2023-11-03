import asyncio
import DataBasePeeker
import bot

DataBases: dict[DataBasePeeker.DataBasePeeker, list[int]] = {}


async def CheckBases():
    while True:
        for db in DataBases.keys():
            state = db.peek()
            if state != 0:
                print("Error")
                await bot.Alert(dbName=db.name, users=DataBases[db])
        await asyncio.sleep(10)


async def main():
    await asyncio.create_task(bot.poll())
    await asyncio.create_task(CheckBases())


if __name__ == "__main__":
    asyncio.run(main())
    print(239)

