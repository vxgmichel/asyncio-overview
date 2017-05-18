import asyncio
from tango.asyncio import DeviceProxy


async def main():
    device = await DeviceProxy('sys/tg_test/1')
    result = await device.read_attribute('ampli')
    print(result.value)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
