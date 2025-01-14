from dataclasses import dataclass

from src.infrastructure.message_brokers.converters import convert_event_to_broker_message
from src.services.events.base import BaseEvent, EventHandler


@dataclass
class Metadata:
    priority: str
    timestamp: str


@dataclass
class Event:
    type: str
    order_id: str


@dataclass
class RequestToAssistant(BaseEvent):
    type: str
    recipient: str
    subject: str
    body: str
    metadata: Metadata
    event: Event


@dataclass
class RequestToAssistantHandler(EventHandler):
    async def handle(self, event: RequestToAssistant) -> None:
        message_bytes = convert_event_to_broker_message(event)

        await self.message_broker.send_message(
            key=event.type,
            topic=self.broker_topic,
            value=message_bytes
        )
