"""The module responsible for the fixtures for the tests."""

from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Session, engine
from src.db.models import Base
from src.db.repositories import PostgresWalletRepository


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[None, None]:
    """Drop and raise the base before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


@pytest_asyncio.fixture()
async def session(db) -> AsyncGenerator[AsyncSession, None]:
    """Wrap queries in a transaction and return the session object."""
    async with Session() as session_:
        try:
            yield session_
        except Exception as exc:
            await session_.rollback()
            raise exc


@pytest.fixture
def rep(session: AsyncSession) -> Generator[PostgresWalletRepository, None, None]:
    """Return the TaskRepository object."""
    yield PostgresWalletRepository(session)
