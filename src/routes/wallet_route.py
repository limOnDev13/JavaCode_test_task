"""The module responsible for the endpoints related to the tasks."""

import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.db.repositories import BaseWalletRepository, PostgresWalletRepository
from src.schemas.schemas import OperationSchema

logger = logging.getLogger("main_logger.router")

router: APIRouter = APIRouter(
    tags=["wallets"],
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
    wallet_uuid: str,
    operation: OperationSchema,
    wallet_rep: Annotated[BaseWalletRepository, Depends(PostgresWalletRepository)],
):
    """Update the wallet or create a new."""
    try:
        w_uuid: uuid.UUID = uuid.UUID(wallet_uuid)
    except ValueError:
        logger.warning("Wallet uuid is not valid.")
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "Wallet uuid is not valid.",
                "input": wallet_uuid,
            },
        )
    else:
        try:
            _, was_updated = await wallet_rep.update_or_create(w_uuid, operation)
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
