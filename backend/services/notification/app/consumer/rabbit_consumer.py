import json
import aio_pika
from typing import Callable, Awaitable

from .base import BaseConsumer
from ..models.consumers.rabbit import RabbitConsumerSettings
from ..models.notification_message.union import NotificationMessage
from ..utils.log import Log

class RabbitConsumer(BaseConsumer[RabbitConsumerSettings]):
    """
    RabbitMQ consumer implementation for NotificationMessage.
    """
    def __init__(
        self,
        settings: RabbitConsumerSettings,
        callback: Callable[[NotificationMessage], Awaitable[None]]
    ):
        super().__init__(settings, callback)
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.RobustChannel | None = None
        self._queue: aio_pika.RobustQueue | None = None

    async def start(self):
        """Establish connection and start listening."""
        self._connection = await aio_pika.connect_robust(
            host=self.settings.host,
            port=self.settings.port,
            login=self.settings.username,
            password=self.settings.password,
            loop=self.loop
        )

        self._channel = await self._connection.channel()

        # prevent consumer from being flooded
        await self._channel.set_qos(prefetch_count=10)

        self._queue = await self._channel.declare_queue(
            self.settings.queue_name,
            durable=True
        )

        Log.info(f"[RabbitConsumer] Listening on queue: {self.settings.queue_name}")

        self.loop.create_task(
            self._queue.consume(self._on_message, no_ack=False)
        )

    async def _on_message(self, message: aio_pika.IncomingMessage):
        async with message.process(requeue=False):
            try:
                raw_body = message.body.decode()
                data = json.loads(raw_body)

                notif_message: NotificationMessage  = NotificationMessage.model_validate(data)

                # Forward to dispatcher/handler logic
                await self.callback(notif_message)

            except Exception as e:
                Log.error(f"[RabbitConsumer] Error processing message: {e}")
                # message will not be requeued because of requeue=False
                # you may add a dead-letter exchange in Rabbit settings

    async def close(self):
        """Gracefully close the connection."""
        if self._connection:
            await self._connection.close()
            Log.info("[RabbitConsumer] Connection closed")
