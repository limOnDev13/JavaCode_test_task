"""The module responsible for pushing the redis connection to each handler."""

import redis.asyncio as redis
from fastapi import FastAPI, Request, Response
from redis.asyncio.connection import ConnectionPool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.cache.redis_cache import RedisCache


class RedisCacheMiddleware(BaseHTTPMiddleware):
    """The middleware responsible for pushing the connection to the handlers."""

    def __init__(self, app: FastAPI, redis_pool: ConnectionPool):
        """Initialize middleware."""
        super().__init__(app)
        self.__pool = redis_pool

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Take a connection from the pool and add it to the request.state.cache."""
        async with redis.Redis.from_pool(self.__pool) as client:
            await client.ping()
            request.state.cache = RedisCache(client)
            return await call_next(request)
