"""The module responsible for pydantic schemes."""

from typing import Set

from pydantic import BaseModel, Field, field_validator

OPERATION_TYPES: Set[str] = {"DEPOSIT", "WITHDRAW"}


class UpdateWalletSchema(BaseModel):
    """The scheme for conducting operations with the wallet."""

    operationType: str = Field(
        ...,
        description="The type of operation with the wallet."
        " The value must be in OPERATION_TYPES.",
    )
    amount: int = Field(
        ...,
        description="The amount of the currency unit that the operation"
        " is being performed with. The value must be non-negative.",
        ge=0,
    )

    @field_validator("operationType", mode="after")
    @classmethod
    def validate_operation_type(cls, value: str) -> str:
        """Validate the field operationType."""
        if value not in OPERATION_TYPES:
            raise ValueError(
                f"operationType must be in {OPERATION_TYPES}."
                f" The received value is {value}"
            )
        return value
