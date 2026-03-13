import json
import aio_pika
from core.config import settings

async def publish_click(click_data: dict):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            "click_events",
            durable=True
        )

        message = aio_pika.Message(
            body=json.dumps(click_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name
        )