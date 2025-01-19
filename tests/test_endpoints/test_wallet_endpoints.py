"""A module for testing endpoints related to the wallet."""

import random
from string import ascii_letters
from typing import List
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from src.schemas.schemas import OperationSchema


@pytest.mark.asyncio
async def test_post_wallets_operation_send_incr_wallet(
    client: AsyncClient,
    operation_inc: OperationSchema,
):
    """Test sending a wallet augmentation operation to a wallet."""
    random_uuid: UUID = uuid4()

    # not existing wallet
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation_inc.model_dump()
    )
    assert response.status_code == 201

    # existing wallet
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation_inc.model_dump()
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_wallets_operation_send_decr_wallet(
    client: AsyncClient, operation_inc: OperationSchema, operation_dec: OperationSchema
):
    """Test sending a wallet reduction operation."""
    random_uuid: UUID = uuid4()

    # not existing wallet
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation_inc.model_dump()
    )
    assert response.status_code == 201

    # existing wallet
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation_dec.model_dump()
    )
    assert response.status_code == 200

    # Trying to make a negative balance
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation_dec.model_dump()
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_post_wallets_operation_invalid_data(
    client: AsyncClient, operation_inc: OperationSchema
):
    """Test sending invalid data."""
    # invalid uuid
    invalid_uuid: str = "".join(
        random.choices(random.choices(ascii_letters, k=random.randint(1, 10)))
    )
    response = await client.post(
        f"/api/v1/wallets/{invalid_uuid}/operation", json=operation_inc.model_dump()
    )
    assert response.status_code == 400

    # invalid operation schema
    random_uuid: UUID = uuid4()
    invalid_data = {"invalid_key": "invalid_value"}
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=invalid_data
    )
    assert response.status_code == 422

    # invalid operation type
    invalid_data = operation_inc.model_dump()
    invalid_data["operationType"] = "".join(
        random.choices(random.choices(ascii_letters, k=random.randint(1, 10)))
    )
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=invalid_data
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_wallets_operation_random_order(
    client: AsyncClient, list_random_operations: List[OperationSchema]
):
    """Test a random sequence of random operations."""
    random_uuid: UUID = uuid4()
    for operation in list_random_operations:
        response = await client.post(
            f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation.model_dump()
        )
        assert 200 <= response.status_code < 300 or 400 <= response.status_code < 500


@pytest.mark.asyncio
async def test_get_wallet_amount(
    client: AsyncClient,
    operation_inc: OperationSchema,
):
    """Test the endpoint GET /api/v1/wallets/{wallet_uuid}."""
    # not existing wallet
    random_uuid: UUID = uuid4()
    response = await client.get(f"/api/v1/wallets/{random_uuid}")
    assert response.status_code == 404

    # create a new wallet
    response = await client.post(
        f"/api/v1/wallets/{str(random_uuid)}/operation", json=operation_inc.model_dump()
    )
    assert response.status_code == 201

    # get existing wallet
    response = await client.get(f"/api/v1/wallets/{random_uuid}")
    assert response.status_code == 200
    assert response.json()["amount"] == operation_inc.amount


@pytest.mark.asyncio
async def test_get_wallet_amount_with_invalid_uuid(
    client: AsyncClient,
):
    """Test the endpoint GET /api/v1/wallets/{wallet_uuid} with invalid uuid."""
    # not existing wallet
    invalid_uuid: str = "".join(
        random.choices(random.choices(ascii_letters, k=random.randint(1, 10)))
    )
    response = await client.get(f"/api/v1/wallets/{invalid_uuid}")
    assert response.status_code == 400
