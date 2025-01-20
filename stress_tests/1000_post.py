"""The module responsible for load testing of sending multiple post requests."""

import asyncio
import random
import time
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

import httpx
from httpx import Response

from src.schemas.schemas import OperationSchema
from src.services.wallet_operations import WalletOperations


async def post_request_to_server(url: str, data: Dict[str, Any]) -> httpx.Response:
    """Make a POST request."""
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=data)


async def ordered_requests_to_single_wallet(
    uuid: UUID, num_operation: int
) -> List[Response]:
    """Collect consecutive requests to a single wallet."""
    operations: List[OperationSchema] = create_operations(num_operation)
    url: str = f"http://localhost:8000/api/v1/wallets/{str(uuid)}/operation"

    responses: List[Response] = list()
    for operation in operations:
        response = await post_request_to_server(url, operation.model_dump())
        responses.append(response)

    return responses


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


async def thousand_post_of_pain(
    num_requests: int = 1000, num_uuids: int = 50, output_file: Optional[str] = None
):
    """Send multiple POST requests asynchronously."""
    uuids: List[UUID] = create_uuids(num_uuids)
    list_uuids = [random.choice(uuids) for _ in range(num_requests)]
    dict_uuids = {uuid_: list_uuids.count(uuid_) for uuid_ in uuids}

    start_time = time.time()

    tasks = [
        ordered_requests_to_single_wallet(uuid_, uuid_count)
        for uuid_, uuid_count in dict_uuids.items()
    ]

    responses_lists: List[List[Response]] = await asyncio.gather(*tasks)

    end_time = time.time()

    responses: List[Response] = list()
    for item in responses_lists:
        responses.extend(item)

    success_count: int = 0
    msg: str = ""
    for i, resp in enumerate(responses):
        status = resp.status_code
        if 200 <= status < 300 or 400 <= status < 500:
            msg += f"{i}: {status}\n"
            success_count += 1
        else:
            msg += f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{i}: {status}\n"

    msg += f"Time of requests and responses received: {end_time - start_time}\n"
    msg += f"Number of successful requests: {success_count} / {num_requests}\n"
    average_time: float = round((end_time - start_time) / num_requests, 2)
    msg += f"Average query execution time: {average_time}\n"

    print(msg)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(msg)


if __name__ == "__main__":
    thousand_pain: int = 1000
    asyncio.run(thousand_post_of_pain(thousand_pain, 5))
