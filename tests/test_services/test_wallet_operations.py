"""The module responsible for testing wallet operations."""

import random
from typing import Any, Dict, Set

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
