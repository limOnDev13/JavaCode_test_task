"""The module responsible for configuring the connection to the database."""

from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.config.app_config import Config

logger = getLogger("main_logger.db")

config = Config()

engine: AsyncEngine = create_async_engine(
    config.db.url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=5,
    pool_timeout=60,
)
Session = async_sessionmaker(bind=engine)


async def dependency_session():
    """Create async pool connections and yield it."""
    async with Session() as session:
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        else:
            logger.debug("The transaction was completed successfully.")
            await session.commit()
