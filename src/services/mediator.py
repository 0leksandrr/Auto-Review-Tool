import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

import redis.asyncio as aioredis

from src.services.commands.base import CT, BaseCommand
from src.services.events.base import EventHandler, ET
from src.services.github_client_service import GitHubClient
from src.services.gpt_client_service import OpenAIClient, CodeAnalyzer
from src.utils.logger import logger


class CommandHandler:
    pass


@dataclass
class Mediator:
    github_client: GitHubClient
    ai_client: OpenAIClient
    redis_client: aioredis.Redis

    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_command(self, command: CT, command_handlers: Iterable):
        self.commands_map[command].extend(command_handlers)

    def register_event(self, event: ET, event_handlers: Iterable):
        self.events_map[event].extend(event_handlers)

    async def handle_command(self, command: BaseCommand) -> Iterable:
        command_type = command.__class__
        handlers = self.commands_map[command_type]

        return [await handler.handle(command) for handler in handlers]

    async def handle_event(self, event: ET) -> Iterable:
        event_type = event.__class__
        handlers = self.events_map[event_type]

        return [await handler.handle(event) for handler in handlers]

    async def generate_review(
            self,
            github_repo_url: str,
            assignment_description: str,
            candidate_level: str
    ) -> dict[str, str]:
        cache_key = f"review_{github_repo_url}_{candidate_level}_{assignment_description}"

        cached_review = await self.redis_client.get(cache_key)
        if cached_review:
            logger.info(f"Cache hit for {github_repo_url}")
            return json.loads(cached_review)

        logger.info(f"Generating review for {github_repo_url}")
        repo_contents = await self.github_client.handle(github_repo_url)

        if not repo_contents:
            raise Exception("No files found in the repository.")

        analyzer = CodeAnalyzer(self.ai_client, assignment_description, candidate_level)
        result = await analyzer.analyze(repo_contents)

        await self.redis_client.setex(cache_key, 600, json.dumps(result))
        logger.info(f"Review cached for {github_repo_url}")

        return result
