from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from openai import AsyncOpenAI


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...


CT = TypeVar('CT', bound=BaseCommand)
CR = TypeVar('CR', bound=Any)


@dataclass(frozen=True)
class BaseCommandHandler(ABC, Generic[CT, CR]):

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...

    async def ai_request(
            self,
            client: AsyncOpenAI,
            model: str,
            system_description: str,
            prompt: str,
            **kwargs
    ) -> str:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_description},
                {"role": "user", "content": prompt},
            ],
            **kwargs
        )

        return response.choices[0].message.content
