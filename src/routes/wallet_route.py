"""The module responsible for the endpoints related to the tasks."""

import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.db.repositories import BaseWalletRepository, PostgresWalletRepository
from src.schemas.schemas import OperationSchema, WalletSchema
from src.utils.uuid_validating import validate_uuid

logger = logging.getLogger("main_logger.router")

router: APIRouter = APIRouter(
    tags=["wallets"],
    dependencies=[Depends(validate_uuid)],
)


@router.post(
    "/api/v1/wallets/{wallet_uuid}/operation",
    status_code=200,
    responses={
        200: {
            "description": "The wallet was updated",
            "content": {"application/json": {"example": {"msg": "OK"}}},
        },
        201: {
            "description": "The wallet was not found,"
            " so a new one was created with a zero account"
            " and the operation was already performed with it.",
            "content": {"application/json": {"example": {"msg": "OK"}}},
        },
        400: {
            "description": "An invalid operation was selected or "
            "invalid operation parameters were passed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "msg": "Wallet uuid is not valid.",
                            "input": "uuid",
                        }
                    }
                }
            },
        },
    },
)
async def update_wallet(
    request: Request,
    operation: OperationSchema,
    wallet_rep: Annotated[BaseWalletRepository, Depends(PostgresWalletRepository)],
):
    """Update the wallet or create a new."""
    try:
        wallet_uuid: UUID = request.state.uuid  # from global dependency
        _, was_updated = await wallet_rep.update_or_create(wallet_uuid, operation)
    except Exception as exc:
        logger.warning(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    else:
        if was_updated:
            return dict(msg="OK")
        else:
            return JSONResponse(
                status_code=201,
                content={"msg": "OK"},
            )


@router.get(
    "/api/v1/wallets/{wallet_uuid}",
    status_code=200,
    response_model=WalletSchema,
    responses={
        400: {
            "description": "Invalid UUID.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "msg": "UUID is not valid.",
                            "input": "uuid",
                        }
                    }
                }
            },
        },
        404: {
            "description": "Wallet not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "msg": "Wallet not found.",
                            "input": "uuid",
                        }
                    }
                }
            },
        },
    },
)
async def get_wallet(
    request: Request,
    wallet_rep: Annotated[BaseWalletRepository, Depends(PostgresWalletRepository)],
):
    """Get the wallet by uuid."""
    wallet_uuid: UUID = request.state.uuid
    wallet: Optional[WalletSchema] = await wallet_rep.get(wallet_uuid)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "Wallet not found.",
                "input": str(wallet_uuid),
            },
        )
    return wallet
