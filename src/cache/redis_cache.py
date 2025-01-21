"""The module responsible for implementing the cache with the backend on redis."""

from logging import getLogger
from typing import Optional
from uuid import UUID

import redis.asyncio as redis

from src.config.app_config import Config

from .base_cache import BaseCache

logger = getLogger("main_logger.cache")


class RedisCache(BaseCache):
    """Cache class with the backend on redis."""

    def __init__(self, client: redis.Redis):
        """Initialize class."""
        logger.debug("Init cache.")
        self.__client = client

    async def get(self, uuid: UUID) -> Optional[int]:
        """Get from cache."""
        logger.debug("Get from cache.")
        return await self.__client.get(str(uuid))

    async def put(self, uuid: UUID, wallet_amount: int) -> None:
        """Put into cache."""
        logger.debug("Put into cache.")
        await self.__client.set(
            str(uuid), str(wallet_amount), ex=Config().redis.cache_timeout
        )

    async def delete(self, uuid: UUID) -> None:
        """Delete from cache."""
        logger.debug("Delete from cache.")
        await self.__client.delete(str(uuid))
