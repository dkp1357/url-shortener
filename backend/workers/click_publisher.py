import json
import aio_pika
from services.analytics import record_click
import services.rabbitmq as rabbitmq_service

async def publish_click(url_id, request):
    click_data = await record_click(url_id, request)

    message = aio_pika.Message(
        body=json.dumps(click_data).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )

    await rabbitmq_service.channel.default_exchange.publish(message, routing_key=rabbitmq_service.queue.name)
