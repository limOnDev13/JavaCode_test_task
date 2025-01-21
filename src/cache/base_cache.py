"""The module responsible for the basic cache interface."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class BaseCache(ABC):
    """The base class of the cache."""

    @abstractmethod
    async def put(self, uuid: UUID, wallet_amount: int) -> None:
        """Put a new wallet with uuid and start wallet_amount."""
        pass

    @abstractmethod
    async def get(self, uuid: UUID) -> Optional[int]:
        """Get wallet amount by uuid."""
        pass

    @abstractmethod
    async def delete(self, uuid: UUID) -> None:
        """Delete wallet from cache."""
        pass
