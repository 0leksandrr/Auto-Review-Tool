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
