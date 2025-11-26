import redis.asyncio as redis
from .base import ResourceInterface
from ..config.redis import RedisConfig
from ..utils.log import Log

class RedisResource(ResourceInterface[RedisConfig]):

    def __init__(self, settings):
        super().__init__(settings)
        self.client = None

    async def initialize(self):
        self.client = redis.from_url(
            self.settings.url,
            db=self.settings.db,
            decode_responses=True
        )
        Log.info(f"[RedisResource] redis client initialized successfully.")

    async def close(self):
        if self.client:
            await self.client.close()
            Log.info(f"[RedisResource] redis client closed successfully.")
