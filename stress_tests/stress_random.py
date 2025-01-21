"""A module for load testing of random requests in threads."""

import logging.config
import random
import time
from threading import Thread
from typing import List, Optional
from uuid import UUID

import requests
from requests import Response

from src.config.log_config import LOG_CONFIG
from src.schemas.schemas import OperationSchema
from src.services.wallet_operations import WalletOperations
from stress_tests.utils import create_uuids, print_results_of_stress_tests

POST_REQUEST_URL = "http://127.0.0.1:8080/api/v1/wallets/{wallet_uuid}/operation"
GET_REQUEST_URL = "http://127.0.0.1:8080/api/v1/wallets/{wallet_uuid}"
OPERATIONS = list(WalletOperations().set_operations)

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("main_logger.stress_tests")


def get_request(uuid: UUID, responses: List[Response]) -> None:
    """Make GET request."""
    logger.info("Send GET request to wallet with %s", str(uuid))
    responses.append(requests.get(GET_REQUEST_URL.format(wallet_uuid=str(uuid))))


def post_request(uuid: UUID, responses: List[Response]) -> None:
    """Make POST request."""
    logger.info("Make POST request to wallet with uuid %s", str(uuid))
    operation: OperationSchema = OperationSchema(
        operationType=random.choice(OPERATIONS), amount=random.randint(0, 1000)
    )
    print(operation)
    responses.append(
        requests.post(
            POST_REQUEST_URL.format(wallet_uuid=str(uuid)), json=operation.model_dump()
        )
    )


def thousand_random_of_pain(
    num_requests: int, num_uuids: int, output_file: Optional[str] = None
) -> None:
    """Send multiple POST requests asynchronously."""
    logger.info(
        "Start stress test with num requests %d and num wallets %d",
        num_requests,
        num_uuids,
    )
    logger.info("Generating uuids...")
    uuids: List[UUID] = create_uuids(num_uuids)

    logger.info("Start sending requests.")

    start_time = time.time()

    responses: List[Response] = list()
    threads: List[Thread] = [
        Thread(
            target=random.choice((get_request, post_request)),
            args=(random.choice(uuids), responses),
        )
        for _ in range(num_requests)
    ]

    for thread_ in threads:
        thread_.start()

    for thread_ in threads:
        thread_.join()

    end_time = time.time()
    logger.info("Responses were received.")

    print_results_of_stress_tests(
        num_requests=num_requests,
        num_uuids=num_uuids,
        method="RANDOM",
        responses=responses,
        start_time=start_time,
        end_time=end_time,
        output_file=output_file,
    )


if __name__ == "__main__":
    thousand_pain: int = 1000
    num_users: int = 5
    thousand_random_of_pain(
        num_requests=thousand_pain,
        num_uuids=num_users,
        output_file=f"./results/random/stress_random_{num_users}_{thousand_pain}.txt",
    )
