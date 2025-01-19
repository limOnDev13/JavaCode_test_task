"""A module for testing endpoints related to the wallet."""

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
