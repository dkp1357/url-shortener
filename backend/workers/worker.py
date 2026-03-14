import asyncio
from workers.click_consumer import consume_click


async def main():
    print("Worker started. Waiting for click events...")
    await consume_click()


if __name__ == "__main__":
    asyncio.run(main())
