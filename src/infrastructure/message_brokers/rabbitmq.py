import orjson
import aio_pika
from dataclasses import dataclass

from src.infrastructure.message_brokers.base import BaseMessageBroker
from src.utils.logging import logger


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    connection_url: str
    connection: aio_pika.RobustConnection | None = None
    channel: aio_pika.abc.AbstractChannel | None = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        self.channel = await self.connection.channel()
        logger.info("RabbitMQ connection and channel established.")

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.info("RabbitMQ connection and channel closed.")

    async def send_message(self, key: str, topic: str, value: bytes):
        if not self.channel:
            raise RuntimeError("RabbitMQ channel is not initialized. Call start() first.")

        exchange = await self.channel.declare_exchange(topic, aio_pika.ExchangeType.DIRECT)
        message = aio_pika.Message(body=value)
        await exchange.publish(message, routing_key=key)
        logger.info(f"Message sent to exchange '{topic}' with routing key '{key}'.")
