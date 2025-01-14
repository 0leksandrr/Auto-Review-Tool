import orjson

from src.services.events.base import BaseEvent


def convert_event_to_broker_message(event: BaseEvent) -> bytes:
    return orjson.dumps(event, default=lambda o: o.__dict__)
