from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class BaseCache:
    @abstractmethod
    async def get(self, key: str) -> str | None:
        ...

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int) -> None:
        ...

    @abstractmethod
    async def lpush(self, key: str, *values: str) -> None:
        ...

    @abstractmethod
    async def lrange(self, key: str, start: int, end: int) -> list[str]:
        ...

    @abstractmethod
    async def expire(self, key: str, ttl: int) -> None:
        ...
