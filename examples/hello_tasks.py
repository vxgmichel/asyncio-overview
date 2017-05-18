import asyncio


async def say(what, when):
    await asyncio.sleep(when)
    print(what)


loop = asyncio.get_event_loop()
loop.create_task(say('First hello!', 2))
loop.create_task(say('Second hello!', 1))
loop.run_forever()
