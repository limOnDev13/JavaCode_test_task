"""The module responsible for testing repositories."""

import random
from string import ascii_letters
from typing import Optional
from uuid import UUID, uuid4

import pytest

from src.db.repositories import PostgresWalletRepository
from src.schemas.schemas import OperationSchema, WalletSchema


@pytest.mark.asyncio
async def test_wallet_repository_update_or_create_with_incr_operation(
    rep: PostgresWalletRepository,
    operation_inc: OperationSchema,
) -> None:
    """Test PostgresWalletRepository method update_or_create with increase operation."""
    # new wallet
    random_uuid: UUID = uuid4()
    wallet_amount, was_updated = await rep.update_or_create(
        uuid=random_uuid,
        new_data=operation_inc,
    )
    assert wallet_amount == operation_inc.amount
    assert was_updated is False

    # update wallet
    wallet_amount, was_updated = await rep.update_or_create(
        uuid=random_uuid,
        new_data=operation_inc,
    )
    assert wallet_amount == 2 * operation_inc.amount
    assert was_updated is True


@pytest.mark.asyncio
async def test_wallet_repository_update_or_create_with_decr_operation(
    rep: PostgresWalletRepository,
    operation_inc: OperationSchema,
    operation_dec: OperationSchema,
) -> None:
    """Test PostgresWalletRepository.update_or_create with reduction operation."""
    # new wallet
    random_uuid: UUID = uuid4()
    wallet_amount, was_updated = await rep.update_or_create(
        uuid=random_uuid,
        new_data=operation_inc,
    )
    assert wallet_amount == operation_inc.amount
    assert was_updated is False

    # update wallet
    wallet_amount, was_updated = await rep.update_or_create(
        uuid=random_uuid,
        new_data=operation_dec,
    )
    assert wallet_amount == 0
    assert was_updated is True

    # trying to make a negative balance
    with pytest.raises(ValueError):
        await rep.update_or_create(
            uuid=random_uuid,
            new_data=operation_dec,
        )


@pytest.mark.asyncio
async def test_wallet_repository_update_or_create_with_invalid_operation(
    rep: PostgresWalletRepository, operation_inc: OperationSchema
) -> None:
    """Test PostgresWalletRepository.update_or_create with invalid operation."""
    random_operation: str = "".join(
        random.choices(ascii_letters, k=random.randint(1, 10))
    )
    random_uuid: UUID = uuid4()
    operation_inc.operationType = random_operation

    with pytest.raises(KeyError):
        await rep.update_or_create(
            uuid=random_uuid,
            new_data=operation_inc,
        )


@pytest.mark.asyncio
async def test_wallet_repository_get(
    rep: PostgresWalletRepository, operation_inc: OperationSchema
):
    """Test the method PostgresWalletRepository.get."""
    random_uuid: UUID = uuid4()
    # get not existing wallet
    result: Optional[WalletSchema] = await rep.get(random_uuid)
    assert result is None

    wallet_amount, was_updated = await rep.update_or_create(
        uuid=random_uuid,
        new_data=operation_inc,
    )
    assert was_updated is False
    # get existing wallet
    result = await rep.get(random_uuid)
    assert isinstance(result, WalletSchema)
    assert result.amount == wallet_amount
    assert result.uuid == random_uuid
