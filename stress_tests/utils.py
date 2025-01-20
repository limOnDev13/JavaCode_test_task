"""The module with auxiliary functions"""

import random
from typing import List, Set
from uuid import UUID, uuid4

from src.schemas.schemas import OperationSchema
from src.services.wallet_operations import WalletOperations


def create_uuids(number: int = 100) -> List[UUID]:
    """Generate a list of uuids."""
    return [uuid4() for _ in range(number)]


def create_operations(num_operations: int = 1000) -> List[OperationSchema]:
    """Generate a list of operations to the wallet."""
    wallet_operations: Set[str] = WalletOperations().set_operations
    return [
        OperationSchema(
            operationType=random.choice(list(wallet_operations)),
            amount=random.randint(0, 1000),
        )
        for _ in range(num_operations)
    ]
