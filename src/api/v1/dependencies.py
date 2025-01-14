from httpx import AsyncClient
from openai import AsyncOpenAI
from punq import Container, Scope
import redis.asyncio as aioredis
from redis.asyncio import Redis

from src.services.commands.assistant import AssistCommandHandler, AssistCommand
from src.services.github_client_service import GitHubClient
from src.services.gpt_client_service import OpenAIClient, CodeAnalyzer
from src.services.mediator import Mediator
from src.utils.config import settings


def init_container() -> Container:
    container = Container()

    container.register(
        Redis,
        lambda: aioredis.from_url(
            settings.REDIS_URL,
            encoding='utf-8',
            decode_responses=True
        ),
        scope=Scope.singleton
    )

    container.register(AsyncOpenAI, lambda: AsyncOpenAI(
        base_url=settings.OPENAI_URL,
        api_key=settings.OPENAI_API_KEY)
    )

    container.register(
        GitHubClient,
        lambda: GitHubClient(
            base_url=settings.GITHUB_URL,
            token=settings.GITHUB_TOKEN
        ),
        scope=Scope.singleton
    )

    container.register(
        OpenAIClient,
        lambda: OpenAIClient(
            client=container.resolve(AsyncOpenAI),
            base_url=settings.OPENAI_URL,
            token=settings.OPENAI_API_KEY
        ),
        scope=Scope.singleton
    )

    def init_mediator() -> Mediator:
        mediator = Mediator(
            github_client=container.resolve(GitHubClient),
            ai_client=container.resolve(OpenAIClient),
            redis_client=container.resolve(Redis),
        )

        create_assistant_handler = AssistCommandHandler(
            client=container.resolve(AsyncOpenAI),
        )

        mediator.register_command(
            AssistCommand,
            [create_assistant_handler,]
        )

        return mediator

    container.register(
        Mediator,
        factory=init_mediator,
        scope=Scope.singleton
    )

    return container
