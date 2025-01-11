import asyncio
import time
from dataclasses import dataclass

import httpx

from src.services.base import BaseAPIClient
from src.utils.config import settings


@dataclass
class GitHubClient(BaseAPIClient):

    async def _fetch_data(self, url: str, as_json: bool = True) -> dict | str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {self.token}"})

            remaining_requests = int(response.headers.get("X-RateLimit-Remaining", 1))
            if remaining_requests == 0:
                reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
                wait_time = reset_time - int(time.time()) + 1
                print(f"Rate limit hit. Retrying after {wait_time} seconds.")
                await asyncio.sleep(wait_time)
                return await self._fetch_data(url, as_json)

            response.raise_for_status()

            if as_json:
                return response.json()
            return response.text

    async def process_directory(self, github_url: str) -> list[dict]:
        files = []
        items = await self._fetch_data(github_url, as_json=True)

        IGNORE_FILES = settings.IGNORE_FILES.split(",")

        for item in items:
            if item["type"] == "file" and item["name"] not in IGNORE_FILES:
                content = await self._fetch_data(item["download_url"], as_json=False)
                if content:
                    files.append({"name": item["path"], "content": content})
            elif item["type"] == "dir":
                files.extend(await self.process_directory(item["url"]))

        return files

    async def handle(self, repo_url: str) -> list[dict]:
        repo_path = repo_url.replace("https://github.com/", "").strip()
        api_url = f"https://api.github.com/repos/{repo_path}/contents/"

        return await self.process_directory(api_url)
