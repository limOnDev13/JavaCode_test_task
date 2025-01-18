"""The module responsible for configuring the connection to the database."""

from logging import getLogger

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from src.config.app_config import Config

logger = getLogger("main_logger.db")

db_config = Config().db

engine: AsyncEngine = create_async_engine(db_config.url)
