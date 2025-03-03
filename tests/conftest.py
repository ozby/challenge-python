from collections.abc import AsyncGenerator, Generator

import pytest
from dependency_injector import providers
from mongomock_motor import (  # type: ignore
    AsyncMongoMockClient,
)

from server.di import Container

TEST_PEER_ID = "127.0.0.1:89899"


@pytest.fixture
def container() -> Generator[Container, None, None]:
    container = Container()

    mongo_client: providers.Provider[AsyncMongoMockClient] = providers.Singleton(
        AsyncMongoMockClient
    )

    container.mongo_client.override(mongo_client)

    yield container

    container.mongo_client.reset_override()


@pytest.fixture(autouse=True)
async def mock_mongo(container: Container) -> AsyncGenerator[None, None]:
    mongo_client = container.mongo_client()
    db = mongo_client.synthesia_db
    await db.discussions.delete_many({})
    await db.notifications.delete_many({})
    await db.sessions.delete_many({})
    yield
