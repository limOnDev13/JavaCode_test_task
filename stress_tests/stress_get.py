"""The module responsible for load testing of sending multiple GET requests."""

import asyncio
import random
import time
from typing import List, Optional
from uuid import UUID

import httpx
from httpx import Response

from src.schemas.schemas import OperationSchema
from stress_tests.stress_post import post_request_to_server
from stress_tests.utils import create_uuids


async def get_request_to_server(url: str) -> httpx.Response:
    """Make a GET request."""
    async with httpx.AsyncClient() as client:
        return await client.get(url)


async def ordered_get_requests_to_single_wallet(
    uuid: UUID, num_requests_from_one: int
) -> List[Response]:
    """Collect consecutive requests to a single wallet."""
    url: str = f"http://127.0.0.1:8000/api/v1/wallets/{str(uuid)}"

    responses: List[Response] = list()
    for _ in range(num_requests_from_one):
        response = await get_request_to_server(url)
        responses.append(response)

    return responses


async def thousand_get_of_pain(
    num_requests: int = 1000, num_uuids: int = 50, output_file: Optional[str] = None
):
    """Send multiple GET requests asynchronously."""
    uuids: List[UUID] = create_uuids(num_uuids)
    post_urls: List[str] = [
        f"http://127.0.0.1:8000/api/v1/wallets/{str(wallet_uuid)}/operation"
        for wallet_uuid in uuids
    ]

    # create new wallets
    operation: OperationSchema = OperationSchema(
        operationType="DEPOSIT", amount=random.randint(0, 1000)
    )
    tasks_post = [
        post_request_to_server(url, data=operation.model_dump()) for url in post_urls
    ]
    post_responses: List[Response] = await asyncio.gather(*tasks_post)

    start_time = time.time()

    tasks_get = [
        ordered_get_requests_to_single_wallet(
            uuid_, num_requests_from_one=num_requests // num_uuids
        )
        for uuid_ in uuids
    ]

    get_responses: List[List[Response]] = await asyncio.gather(*tasks_get)
    end_time = time.time()

    responses: List[Response] = post_responses
    for list_responses in get_responses:
        responses.extend(list_responses)

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
    num_users: int = 2
    asyncio.run(
        thousand_get_of_pain(
            thousand_pain, num_users, f"stress_get_{num_users}_{thousand_pain}.txt"
        )
    )
