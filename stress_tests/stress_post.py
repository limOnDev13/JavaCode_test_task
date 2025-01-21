"""The module responsible for load testing of sending multiple POST requests."""

import asyncio
import logging.config
import random
import time
from typing import Any, Dict, List, Optional
from uuid import UUID

import httpx
from httpx import Response, Timeout

from src.config.log_config import LOG_CONFIG
from src.schemas.schemas import OperationSchema
from stress_tests.utils import create_operations, create_uuids

from .utils import print_results_of_stress_tests

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("main_logger.stress_tests")


async def post_request_to_server(url: str, data: Dict[str, Any]) -> httpx.Response:
    """Make a POST request."""
    logger.info("Make POST request to %s", url)
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=data, timeout=Timeout(timeout=300))


async def ordered_post_requests_to_single_wallet(
    uuid: UUID, num_operation: int
) -> List[Response]:
    """Collect consecutive requests to a single wallet."""
    operations: List[OperationSchema] = create_operations(num_operation)
    url: str = f"http://127.0.0.1:8080/api/v1/wallets/{str(uuid)}/operation"

    logger.info("Start sending requests to wallet with uuid %s", str(uuid))
    responses: List[Response] = list()
    for operation in operations:
        response = await post_request_to_server(url, operation.model_dump())
        responses.append(response)
    logger.info("UUID: %s | Done", str(uuid))

    return responses


async def thousand_post_of_pain(
    num_requests: int = 1000, num_uuids: int = 50, output_file: Optional[str] = None
):
    """Send multiple POST requests asynchronously."""
    logger.info(
        "Start stress tests with num requests %d and num wallets %d",
        num_requests,
        num_uuids,
    )
    logger.info("Generating uuids...")
    uuids: List[UUID] = create_uuids(num_uuids)
    list_uuids = [random.choice(uuids) for _ in range(num_requests)]
    dict_uuids = {uuid_: list_uuids.count(uuid_) for uuid_ in uuids}
    logger.info("UUIDs were generated.")

    logger.info("Starting requests.")
    start_time = time.time()

    tasks = [
        ordered_post_requests_to_single_wallet(uuid_, uuid_count)
        for uuid_, uuid_count in dict_uuids.items()
    ]

    responses_lists: List[List[Response]] = await asyncio.gather(*tasks)

    end_time = time.time()
    logger.info("Responses were received.")

    responses: List[Response] = list()
    for item in responses_lists:
        responses.extend(item)

    print_results_of_stress_tests(
        num_requests=num_requests,
        num_uuids=num_uuids,
        method="POST",
        responses=responses,
        start_time=start_time,
        end_time=end_time,
        output_file=output_file,
    )


if __name__ == "__main__":
    thousand_pain: int = 1000
    num_users: int = 1000
    asyncio.run(
        thousand_post_of_pain(
            thousand_pain,
            num_users,
            f"./results/post/stress_post_{num_users}_{thousand_pain}.txt",
        )
    )
