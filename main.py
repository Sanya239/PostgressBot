import asyncio
import DataBasePeeker
import bot
import Solutions

DataBases: dict[DataBasePeeker.DataBasePeeker, list[int]] = {}

async def CheckBases():
    while True:
        for db in DataBases.keys():
            state = db.peek()
            if state == "ok":
                print("Error")
                await bot.Alert(dbName=db.database, users=DataBases[db])
                await Solutions.solutions[state](db=db,users=DataBases[db])
        await asyncio.sleep(10)


async def main():
    await asyncio.create_task(bot.poll())
    await asyncio.create_task(CheckBases())


if __name__ == "__main__":
    asyncio.run(main())
    print(239)

