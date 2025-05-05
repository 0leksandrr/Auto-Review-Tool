import re
import uuid
from dataclasses import dataclass
from datetime import datetime

from openai import AsyncOpenAI

from src.infrastructure.cache.base import BaseCache
from src.services.commands.base import BaseCommand, BaseCommandHandler
from src.services.events.assistant import RequestToAssistant, Metadata, Event
from src.utils.config import settings


URL_PATTERN = r'https?://[^\s]+'
NUMBER_PATTERN = r'/(\d{2,3})/\)$'


@dataclass(frozen=True)
class AssistCommand(BaseCommand):
    description: str
    links: list


@dataclass(frozen=True)
class AssistCommandHandler(BaseCommandHandler):
    client: AsyncOpenAI
    cache: BaseCache

    async def handle(self, command: AssistCommand) -> list:
        cache_key = f"assist_{command.description}_{command.links}"
        cached_review = await self.cache.lrange(cache_key, 0, -1)

        if cached_review:
            numbers = list(map(int, cached_review))
            return numbers

        prompt_template = settings.ASSIST_PROMPT_TEMPLATE
        prompt_template = prompt_template.format(links=command.links, description=command.description)
        result = await self.ai_request(
            client=self.client,
            model=settings.GPT_MODEL_NAME,
            system_description="You are an AI assistant specializing in product recommendations.",
            prompt=prompt_template,
            max_tokens=1000,
        )

        await self._mediator.handle_event(RequestToAssistant(
            type="email",
            recipient="example@gmail.com",
            subject="Order Update Notification",
            body="Dear customer, your order has been processed successfully.",
            metadata=Metadata(
                priority="low",
                timestamp=datetime.now().isoformat()
            ),
            event=Event(type="request_to_assistant", order_id=str(uuid.uuid4())),
        ))

        urls = re.findall(URL_PATTERN, result)
        numbers_from_urls = []

        for url in urls:
            match = re.search(NUMBER_PATTERN, url)
            if match:
                numbers_from_urls.append(match.group(1))

        if numbers_from_urls:
            await self.cache.lpush(cache_key, *map(str, numbers_from_urls))
            await self.cache.expire(cache_key, 600)

        return numbers_from_urls
