import aio_pika
from core.config import settings

connection = None
channel = None
queue = None


async def connect_rabbitmq():
    global connection, channel, queue
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("click_events", durable=True)


async def close_rabbitmq():
    await connection.close()
