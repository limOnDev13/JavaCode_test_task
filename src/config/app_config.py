"""The module responsible for the application configuration."""

import os
from dataclasses import dataclass, field

import dotenv

# TODO - Figure out how to load environment variables in a smart way
#  - for example, make a download in a coroutine with a delay and wrap it with a task.
dotenv.load_dotenv()


@dataclass
class DB(object):
    """Config class for the database."""

    user: str = os.getenv("POSTGRES_USER", "user")
    password: str = os.getenv("POSTGRES_PASSWORD", "password")
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: str = os.getenv("POSTGRES_PORT", "5432")
    db_name: str = os.getenv("POSTGRES_DB", "db")
    url: str = os.getenv("POSTGRES_URL", "")

    def __init__(self):
        """Initialize the class."""
        if os.getenv("DEBUG", "0") == "1":
            self.url = os.getenv("POSTGRES_TEST_URL", "")

        if self.url == "":
            self.url = (
                f"postgresql+asyncpg://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.db_name}"
            )


@dataclass
class RedisConfig(object):
    """Config class for the redis."""

    url: str = os.getenv("REDIS_URL", "redis://localhost")
    cache_timeout: int = int(os.getenv("CACHE_TIMEOUT", "60"))


@dataclass
class Config(object):
    """Config class for the app."""

    debug: bool = os.getenv("DEBUG", "0") == "1"
    db: DB = field(default_factory=DB)
    redis: RedisConfig = field(default_factory=RedisConfig)
