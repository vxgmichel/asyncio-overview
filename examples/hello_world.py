import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)


loop = asyncio.get_event_loop()
coro = say('Hello world!', 1)
loop.run_until_complete(coro)
loop.close()
