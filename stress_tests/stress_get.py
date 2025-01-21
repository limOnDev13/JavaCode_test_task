"""The module responsible for load testing of sending multiple GET requests."""

import asyncio
import logging.config
import random
import time
from typing import List, Optional
from uuid import UUID

from httpx import AsyncClient, Response, Timeout

from src.config.log_config import LOG_CONFIG
from src.schemas.schemas import OperationSchema
from stress_tests.stress_post import post_request_to_server
from stress_tests.utils import create_uuids, print_results_of_stress_tests

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("main_logger.stress_tests")


async def get_request_to_server(url: str) -> Response:
    """Make a GET request."""
    logger.info("Doing GET requests to %s", url)
    async with AsyncClient() as client:
        return await client.get(url, timeout=Timeout(timeout=300))


async def ordered_get_requests_to_single_wallet(
    uuid: UUID, num_requests_from_one: int
) -> List[Response]:
    """Collect consecutive requests to a single wallet."""
    url: str = f"http://127.0.0.1:8080/api/v1/wallets/{str(uuid)}"

    logger.info("Doing GET requests to wallet with uuid %s", str(uuid))
    responses: List[Response] = list()
    for _ in range(num_requests_from_one):
        response = await get_request_to_server(url)
        responses.append(response)

    return responses


async def thousand_get_of_pain(
    num_requests: int = 1000, num_uuids: int = 50, output_file: Optional[str] = None
):
    """Send multiple GET requests asynchronously."""
    logger.info(
        "Start stress test with num requests %d and num wallets %d",
        num_requests,
        num_uuids,
    )
    logger.info("Generating uuids...")
    uuids: List[UUID] = create_uuids(num_uuids)
    logger.info("Creating new wallets...")
    post_urls: List[str] = [
        f"http://127.0.0.1:8080/api/v1/wallets/{str(wallet_uuid)}/operation"
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

    logger.info("New wallets were created.")
    logger.info("Start sending requests.")

    start_time = time.time()

    tasks_get = [
        ordered_get_requests_to_single_wallet(
            uuid_, num_requests_from_one=num_requests // num_uuids
        )
        for uuid_ in uuids
    ]

    get_responses: List[List[Response]] = await asyncio.gather(*tasks_get)
    end_time = time.time()
    logger.info("Responses were received.")

    responses: List[Response] = post_responses
    for list_responses in get_responses:
        responses.extend(list_responses)

    print_results_of_stress_tests(
        # First, num_uuids of wallet creation requests are made,
        # then num_requests of regular requests.
        num_requests=num_requests + num_uuids,
        num_uuids=num_uuids,
        method="GET",
        responses=responses,
        start_time=start_time,
        end_time=end_time,
        output_file=output_file,
    )


if __name__ == "__main__":
    thousand_pain: int = 1000
    num_users: int = 1
    asyncio.run(
        thousand_get_of_pain(
            thousand_pain,
            num_users,
            f"results/get/stress_get_{num_users}_{thousand_pain}.txt",
        )
    )
