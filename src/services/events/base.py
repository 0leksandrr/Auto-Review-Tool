from abc import ABC, abstractmethod
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import ClassVar, TypeVar, Any, Generic
from uuid import (
    UUID,
    uuid4,
)

from src.infrastructure.message_brokers.base import BaseMessageBroker

ET = TypeVar('ET', bound="BaseEvent")
ER = TypeVar('ER', bound=Any)


@dataclass
class BaseEvent(ABC):
    event_title: ClassVar[str]

    event_id: UUID = field(default_factory=uuid4, kw_only=True)
    occurred_at: datetime = field(default_factory=datetime.now, kw_only=True)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...
