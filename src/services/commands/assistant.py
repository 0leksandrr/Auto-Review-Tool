import re
import uuid
from dataclasses import dataclass
from datetime import datetime

from openai import AsyncOpenAI

from src.services.commands.base import BaseCommand, BaseCommandHandler
from src.services.events.assistant import RequestToAssistant, Metadata, Event
from src.utils.config import settings


@dataclass(frozen=True)
class AssistCommand(BaseCommand):
    description: str
    links: list


@dataclass(frozen=True)
class AssistCommandHandler(BaseCommandHandler):
    client: AsyncOpenAI

    async def handle(self, command: AssistCommand) -> list:
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

        url_pattern = r'https?://[^\s]+'

        urls = re.findall(url_pattern, result)
        return urls
