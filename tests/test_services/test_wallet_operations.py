"""The module responsible for testing wallet operations."""

import random
from string import ascii_letters
from typing import Any, Dict, Set

import pytest

from src.schemas.schemas import OperationSchema
from src.services.wallet_operations import WalletOperations


def test_property_set_operations():
    """Test the getter set_operations."""
    operations_types: Set[str] = {
        "WITHDRAW",
        "DEPOSIT",
    }
    wallet: WalletOperations = WalletOperations()

    assert wallet.set_operations == operations_types


def test_operation_incr(operation_inc: OperationSchema):
    """Test the operation to increase the wallet volume."""
    start_budget: int = random.randint(0, 100)
    wallet: WalletOperations = WalletOperations(start_budget)
    operation_data: Dict[str, Any] = operation_inc.model_dump()

    cur_amount: int = wallet.make_things(
        operation=operation_data.pop("operationType"),
        **operation_data,
    )
    assert cur_amount == start_budget + operation_inc.amount


def test_operation_decr(operation_dec: OperationSchema):
    """Test the operation to reduce the wallet volume."""
    start_budget: int = random.randint(operation_dec.amount, 2 * operation_dec.amount)
    wallet: WalletOperations = WalletOperations(start_budget)
    operation_data: Dict[str, Any] = operation_dec.model_dump()
    operation_name: str = operation_data.pop("operationType")

    cur_amount: int = wallet.make_things(
        operation=operation_name,
        **operation_data,
    )
    assert cur_amount == start_budget - operation_dec.amount

    # Trying to make a negative balance
    operation_data["amount"] = 2 * start_budget
    with pytest.raises(ValueError):
        wallet.make_things(
            operation=operation_name,
            **operation_data,
        )


def test_invalid_operation(operation_inc: OperationSchema):
    """Test the invalid operation."""
    wallet: WalletOperations = WalletOperations()
    operation_data: Dict[str, Any] = operation_inc.model_dump()
    operation_data.pop("operationType")
    invalid_operation: str = "".join(
        random.choices(ascii_letters, k=random.randint(1, 10))
    )

    with pytest.raises(KeyError):
        wallet.make_things(
            operation=invalid_operation,
            **operation_data,
        )
