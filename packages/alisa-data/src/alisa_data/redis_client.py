from redis import asyncio as aioredis

class AlisaRedisClient:
    def __init__(self, url: str):
        self.pool = aioredis.ConnectionPool.from_url(
            url, max_connections=10, decode_responses=True
        )
        self.redis = aioredis.Redis(connection_pool=self.pool)

    async def set_with_log(self, key: str, value: str, ex: int = 60):
        return await self.redis.set(key, value, ex=ex)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def close(self):
        await self.pool.disconnect()