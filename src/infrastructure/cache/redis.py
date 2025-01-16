from dataclasses import dataclass

import orjson
from redis.asyncio import Redis

from src.infrastructure.cache.base import BaseCache


@dataclass
class RedisCache(BaseCache):
    redis_client: Redis

    async def get(self, key: str) -> str | None:
        return await self.redis_client.get(key)

    async def set(self, key: str, value: str, ttl: int) -> None:
        value = orjson.dumps(value)
        await self.redis_client.setex(key, ttl, value)
