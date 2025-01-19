"""The module responsible for working with uuids."""

from logging import getLogger
from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, Path, Request

logger = getLogger("main_logger.utils")


async def validate_uuid(request: Request, wallet_uuid: Annotated[str, Path()]):
    """Check the uuid from url for validity."""
    try:
        w_uuid: UUID = UUID(wallet_uuid)
    except ValueError:
        logger.warning("Wallet uuid is not valid, uuid: %s", wallet_uuid)
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "Wallet uuid is not valid.",
                "input": wallet_uuid,
            },
        )
    else:
        request.state.uuid = w_uuid
