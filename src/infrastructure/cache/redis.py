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

    async def lpush(self, key: str, *values: str) -> None:
        if values:
            await self.redis_client.lpush(key, *values)

    async def lrange(self, key: str, start: int, end: int) -> list[str]:
        return await self.redis_client.lrange(key, start, end)

    async def expire(self, key: str, ttl: int) -> None:
        await self.redis_client.expire(key, ttl)
