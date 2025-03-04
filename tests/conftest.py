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

    db = providers.Singleton(
        lambda client, db_name: client[db_name],
        mongo_client,
        container.config().get("db_name"),
    )

    container.mongo_client.override(mongo_client)
    container.db.override(db)

    yield container

    container.mongo_client.reset_override()


@pytest.fixture(autouse=True)
async def mock_mongo(container: Container) -> AsyncGenerator[None, None]:
    db = container.db()
    await db.discussions.delete_many({})
    await db.notifications.delete_many({})
    await db.sessions.delete_many({})
    yield
