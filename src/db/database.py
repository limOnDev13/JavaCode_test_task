"""The module responsible for configuring the connection to the database."""

from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from fastapi import Request

from src.config.app_config import Config

logger = getLogger("main_logger.db")

config = Config()

engine: AsyncEngine = create_async_engine(
    config.db.url,
    pre_ping=True,
    pool_size=10,
    max_overflow=5,
    timeout=60.0
)
Session = async_sessionmaker()


async def dependency_session(request: Request):
    """Create async pool connections and save it in request.state.pool."""
    async with Session() as session:
        try:
            request.state.session = session
            yield session
        except Exception as exc:
            logger.exception(f"Exception when working with a database:\n{str(exc)}")
            await session.rollback()
        else:
            logger.debug(f"The transaction was completed successfully.")
            await session.commit()
