"""The module responsible for database queries."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Wallet
from src.schemas.schemas import OperationSchema, WalletSchema
from src.services.wallet_operations import WalletOperations

logger = logging.getLogger("main_logger.repositories")


class BaseWalletRepository(ABC):
    """The basic wallet repository."""

    @abstractmethod
    async def update_or_create(self, uuid: UUID, new_data: OperationSchema) -> int:
        """
        Update existing wallet or create a new.

        :param uuid: Wallet UUID.
        :param new_data: The operation data.
        :return: Current wallet volume.
        """
        pass

    @abstractmethod
    async def get(self, uuid: UUID) -> Optional[WalletSchema]:
        """Get the wallet by uuid if it exists, else None."""
        pass


class PostgresWalletRepository(BaseWalletRepository):
    """
    A repository of wallets with a PostgreSQL backend.

    Args:
        session (AsyncSession) - session object.
    """

    def __init__(self, session: AsyncSession):
        """Initialize class."""
        self.__session = session

    async def update_or_create(self, uuid: UUID, new_data: OperationSchema) -> int:
        """Update existing wallet or create a new."""
        wallet: Optional[Wallet] = await self.__session.get(Wallet, uuid)
        new_data_dict: Dict[str, Any] = new_data.model_dump()
        operation: str = new_data_dict.pop("operationType")

        try:
            if wallet:
                wallet_operations: WalletOperations = WalletOperations(wallet.amount)
                wallet.amount = wallet_operations.make_things(
                    operation, **new_data_dict
                )
            else:
                wallet_operations = WalletOperations()
                wallet = Wallet(
                    uuid=uuid,
                    amount=wallet_operations.make_things(operation, **new_data_dict),
                )
                self.__session.add(wallet)
        except (ValueError, KeyError) as exc:
            logger.exception(str(exc))
            raise exc
        else:
            return wallet.amount

    async def get(self, uuid: UUID) -> Optional[WalletSchema]:
        """Get the wallet by uuid if it exists, else None."""
        wallet = await self.__session.get(Wallet, uuid)
        if wallet:
            return WalletSchema.model_validate(wallet)
        return None
