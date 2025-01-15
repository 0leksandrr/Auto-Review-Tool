from src.api.v1.dependencies import init_container
from src.infrastructure.message_brokers.base import BaseMessageBroker


async def init_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.connect()


async def close_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.disconnect()
