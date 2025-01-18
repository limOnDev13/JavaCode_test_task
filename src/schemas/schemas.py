"""The module responsible for pydantic schemes."""

from typing import Set
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.services.wallet_operations import WalletOperations


class WalletSchema(BaseModel):
    """The base scheme of the wallet."""

    uuid: UUID = Field(
        ...,
        description="Wallet UUID",
    )
    amount: int = Field(
        ...,
        description="The number of currency units in the wallet."
        " The value must be non-negative.",
        ge=0,
    )
    model_config = ConfigDict(from_attributes=True)


class OperationSchema(BaseModel):
    """The scheme for conducting operations with the wallet."""

    amount: int = Field(
        ...,
        description="The amount of the currency unit that the operation"
        " is being performed with. The value must be non-negative.",
        ge=0,
    )
    operationType: str = Field(
        ...,
        description="The type of operation with the wallet."
        " The value must be in OPERATION_TYPES.",
    )

    @field_validator("operationType", mode="after")
    @classmethod
    def validate_operation_type(cls, value: str) -> str:
        """Validate the field operationType."""
        set_operations: Set[str] = WalletOperations.set_operations()

        if value not in set_operations:
            raise ValueError(
                f"operationType must be in {set_operations}."
                f" The received value is {value}"
            )
        return value
