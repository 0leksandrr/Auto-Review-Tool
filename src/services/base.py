from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseAPIClient(ABC):
    base_url: str
    token: str

    @abstractmethod
    async def handle(self, endpoint: str) -> dict | None:
        ...
