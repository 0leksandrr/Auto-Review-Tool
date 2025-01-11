from httpx import AsyncClient
from openai import AsyncOpenAI
from punq import Container, Scope
import redis.asyncio as aioredis
from redis.asyncio import Redis

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

    container.register(
        Mediator,
        lambda: Mediator(
            github_client=container.resolve(GitHubClient),
            ai_client=container.resolve(OpenAIClient),
            redis_client=container.resolve(Redis),
        ),
        scope=Scope.singleton
    )

    return container
