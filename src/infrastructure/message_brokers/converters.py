import orjson

from src.services.events.base import BaseEvent


def convert_event_to_broker_message(event: BaseEvent | dict) -> bytes:
    if isinstance(event, dict):
        return orjson.dumps(event)
    elif isinstance(event, BaseEvent):
        return orjson.dumps(event, default=lambda o: o.__dict__)
