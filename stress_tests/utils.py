"""The module with auxiliary functions."""

import random
from typing import List, Literal, Optional, Set
from uuid import UUID, uuid4

import httpx
import requests

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


def print_results_of_stress_tests(
    num_requests: int,
    num_uuids: int,
    method: Literal["GET", "POST", "RANDOM"],
    responses: List[requests.Response] | List[httpx.Response],
    start_time: float,
    end_time: float,
    output_file: Optional[str] = None,
) -> None:
    """Print results of stress tests in console and in file."""
    msg: str = (
        f"Stress tests with method: {method}"
        f"Number of users: {num_uuids}; total number of requests: {num_requests}\n"
    )

    success_count: int = 0
    for i, resp in enumerate(responses):
        status = resp.status_code
        if 200 <= status < 300 or 400 <= status < 500:
            msg += f"{i}: {status}\n"
            success_count += 1
        else:
            msg += f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{i}: {status}\n"

    msg += f"Time of requests and responses received: {end_time - start_time}\n"
    msg += f"Number of successful requests: {success_count} / {num_requests}\n"
    average_time: float = round((end_time - start_time) / num_requests, 5)
    msg += f"Average query execution time: {average_time}\n"

    print(msg)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(msg)
