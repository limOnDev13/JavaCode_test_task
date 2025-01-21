"""The module responsible for pushing the redis connection to each handler."""

import logging

import redis.asyncio as redis
from fastapi import FastAPI, Request, Response
from redis.asyncio.connection import ConnectionPool
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.cache.redis_cache import RedisCache

logger = logging.getLogger("main_logger.middleware")


class RedisCacheMiddleware(BaseHTTPMiddleware):
    """The middleware responsible for pushing the connection to the handlers."""

    def __init__(self, app: FastAPI, redis_pool: ConnectionPool):
        """Initialize middleware."""
        super().__init__(app)
        retry = Retry(ExponentialBackoff(), 3)
        self.__client = redis.Redis(
            connection_pool=redis_pool,
            retry=retry,
            retry_on_error=[RedisError],
            retry_on_timeout=True,
        )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Take a connection from the pool and add it to the request.state.cache."""
        try:
            await self.__client.ping()
            request.state.cache = RedisCache(self.__client)
            return await call_next(request)
        except RedisError as exc:
            logger.warning("Exception in redis:\n%s", str(exc))
            return Response("Internal Server Error", status_code=500)
