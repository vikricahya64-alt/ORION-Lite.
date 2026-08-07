import asyncio
from runtime import ORIONRuntime

async def main():
    print("Sebelum membuat runtime")
    r = ORIONRuntime()
    print("Sesudah membuat runtime")
    await r.start()

asyncio.run(main())
