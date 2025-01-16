from dataclasses import dataclass
from typing import Optional

import aio_pika
from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from src.infrastructure.message_brokers.base import BaseMessageBroker
from src.infrastructure.message_brokers.converters import convert_event_to_broker_message
from src.utils.logging import logger


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    connection_url: str
    connection: AbstractRobustConnection | None = None

    def status(self) -> bool:
        """
            Checks if connection established

            :return: True if connection established
        """
        if self.connection is None:
            return False
        return True

    async def _clear(self) -> None:
        if self.connection:
            await self.connection.close()

        self.connection = None

    async def connect(self) -> None:
        """
        Establish connection with the RabbitMQ

        :return: None
        """
        try:
            self.connection = await connect_robust(self.connection_url)
        except Exception as e:
            await self._clear()
            logger.error(f"Error connecting to RabbitMQ: {str(e)}")

    async def disconnect(self) -> None:
        """
        Disconnect and clear connections from RabbitMQ

        :return: None
        """
        await self._clear()

    async def send_messages(
            self,
            messages: list | dict,
            routing_key: str = "test"
    ) -> None:
        """
            Public message or messages to the RabbitMQ queue.

            :param messages: list or dict with messages objects.
            :param routing_key: Routing key of RabbitMQ, not required. Tip: the same as in the consumer.
        """
        if self.connection is None:
            await self.connect()

        if isinstance(messages, dict):
            messages = [messages]

        async with self.connection:

            channel = await self.connection.channel()
            await channel.declare_queue(routing_key, durable=True)

            for message in messages:

                await channel.default_exchange.publish(
                    Message(convert_event_to_broker_message(message)),
                    routing_key=routing_key,
                )
