from collections.abc import AsyncGenerator, Generator

import pytest
from dependency_injector import providers
from mongomock_motor import AsyncMongoMockClient  # type: ignore

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

    # Reset overrides after tests
    container.mongo_client.reset_override()


# @pytest.fixture(autouse=True)
# async def client_id(container: Container) -> AsyncGenerator[str, None]:
#     session_service = container.session_service()
#     client_id = "tester_client_1"
#     await session_service.get(TEST_PEER_ID, client_id)
#     yield client_id


@pytest.fixture(autouse=True)
async def mock_mongo(container: Container) -> AsyncGenerator[None, None]:
    mongo_client = container.mongo_client()
    db = mongo_client.synthesia_db
    await db.discussions.delete_many({})
    await db.notifications.delete_many({})
    await db.sessions.delete_many({})
    yield
