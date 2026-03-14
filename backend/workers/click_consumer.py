import json
import aio_pika
from db.session import SessionLocal
from models.models import ClickEvent, URL
from core.config import settings


async def consume_click():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("click_events", durable=True)

        async for message in queue:
            async with message.process():
                click_data = json.loads(message.body.decode())

                db = SessionLocal()

                try:
                    url = db.query(URL).filter(URL.id == click_data["url_id"]).first()

                    if url:
                        click_event = ClickEvent(**click_data)
                        db.add(click_event)

                        url.click_count += 1

                        db.commit()

                except Exception as e:
                    print(f"Error processing click event: {e}")
                    db.rollback()

                finally:
                    db.close()
