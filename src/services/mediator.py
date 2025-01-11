from dataclasses import dataclass
import json
import redis.asyncio as aioredis

from src.services.github_client_service import GitHubClient
from src.services.gpt_client_service import OpenAIClient, CodeAnalyzer
from src.utils.logging import logger


@dataclass
class Mediator:
    github_client: GitHubClient
    ai_client: OpenAIClient
    redis_client: aioredis.Redis

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
