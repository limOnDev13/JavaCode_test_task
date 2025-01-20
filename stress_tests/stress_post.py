"""The module responsible for load testing of sending multiple POST requests."""

import asyncio
import random
import time
from typing import Any, Dict, List, Optional
from uuid import UUID

import httpx
from httpx import Response

from src.schemas.schemas import OperationSchema
from stress_tests.utils import create_operations, create_uuids


async def post_request_to_server(url: str, data: Dict[str, Any]) -> httpx.Response:
    """Make a POST request."""
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=data)


async def ordered_post_requests_to_single_wallet(
    uuid: UUID, num_operation: int
) -> List[Response]:
    """Collect consecutive requests to a single wallet."""
    operations: List[OperationSchema] = create_operations(num_operation)
    url: str = f"http://127.0.0.1:8000/api/v1/wallets/{str(uuid)}/operation"

    responses: List[Response] = list()
    for operation in operations:
        response = await post_request_to_server(url, operation.model_dump())
        responses.append(response)

    return responses


async def thousand_post_of_pain(
    num_requests: int = 1000, num_uuids: int = 50, output_file: Optional[str] = None
):
    """Send multiple POST requests asynchronously."""
    msg: str = (
        f"Number of users: {num_uuids}; total number of requests: {num_requests}\n"
    )

    uuids: List[UUID] = create_uuids(num_uuids)
    list_uuids = [random.choice(uuids) for _ in range(num_requests)]
    dict_uuids = {uuid_: list_uuids.count(uuid_) for uuid_ in uuids}

    start_time = time.time()

    tasks = [
        ordered_post_requests_to_single_wallet(uuid_, uuid_count)
        for uuid_, uuid_count in dict_uuids.items()
    ]

    responses_lists: List[List[Response]] = await asyncio.gather(*tasks)

    end_time = time.time()

    responses: List[Response] = list()
    for item in responses_lists:
        responses.extend(item)

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


if __name__ == "__main__":
    thousand_pain: int = 1000
    num_users: int = 5
    asyncio.run(
        thousand_post_of_pain(
            thousand_pain, num_users, f"stress_post_{num_users}_{thousand_pain}.txt"
        )
    )
