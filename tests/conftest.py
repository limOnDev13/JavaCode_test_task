"""The module responsible for the fixtures for the tests."""

import random
from typing import AsyncGenerator, Generator, List

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Session, engine
from src.db.models import Base
from src.db.repositories import PostgresWalletRepository
from src.main import create_app
from src.schemas.schemas import OperationSchema
from src.services.wallet_operations import WalletOperations


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


@pytest.fixture
def operation_inc() -> OperationSchema:
    """Return the test operation schema to increase the wallet."""
    return OperationSchema(
        amount=10,
        operationType="DEPOSIT",
    )


@pytest.fixture
def operation_dec() -> OperationSchema:
    """Return the test operation schema to decrease the wallet."""
    return OperationSchema(
        amount=10,
        operationType="WITHDRAW",
    )


@pytest.fixture
def random_operation() -> OperationSchema:
    """Return the test operation schema to decrease the wallet."""
    return OperationSchema(
        amount=random.randint(0, 100),
        operationType=random.choice(list(WalletOperations().set_operations)),
    )


@pytest.fixture
def list_random_operations() -> List[OperationSchema]:
    """Return the list of random operation schemas."""
    return [
        OperationSchema(
            amount=random.randint(0, 100),
            operationType=random.choice(list(WalletOperations().set_operations)),
        )
        for _ in range(random.randint(1, 100))
    ]


@pytest.fixture()
def test_app(db) -> Generator[FastAPI, None, None]:
    """Create a test_app with overridden dependencies."""
    _app: FastAPI = create_app()
    yield _app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://localhost:8000"
    ) as client:
        yield client
