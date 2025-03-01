from collections.abc import Generator, AsyncGenerator
from typing import cast

import pytest
from dependency_injector import containers, providers
from mongomock_motor import AsyncMongoMockClient  # type: ignore

from server.di import container as app_container
from server.services.discussion_service import DiscussionService
from server.services.notification_service import NotificationService
from server.services.session_service import SessionService


class MockContainer(containers.DeclarativeContainer):
    mongo_client: providers.Provider[AsyncMongoMockClient] = providers.Singleton(
        AsyncMongoMockClient
    )

    notification_service = providers.Singleton(
        NotificationService, 
        mongo_client=mongo_client
    )

    discussion_service = providers.Singleton(
        DiscussionService, 
        mongo_client=mongo_client, 
        notification_service=notification_service
    )
    
    session_service = providers.Singleton(
        SessionService,
        mongo_client=mongo_client
    )


@pytest.fixture(scope="session")
def container() -> Generator[MockContainer, None, None]:
    # Create our test container
    test_container = MockContainer()

    # Override the application container's providers with test providers
    app_container.mongo_client.override(test_container.mongo_client)
    app_container.notification_service.override(test_container.notification_service)
    app_container.discussion_service.override(test_container.discussion_service)
    app_container.session_service.override(test_container.session_service)

    yield test_container

    # Reset overrides after tests
    app_container.mongo_client.reset_override()
    app_container.notification_service.reset_override()
    app_container.discussion_service.reset_override()
    app_container.session_service.reset_override()


@pytest.fixture
def discussion_service(container: MockContainer) -> DiscussionService:
    return container.discussion_service()


@pytest.fixture
def notification_service(container: MockContainer) -> NotificationService:
    return container.notification_service()


@pytest.fixture
def session_service(container: MockContainer) -> SessionService:
    return container.session_service()


@pytest.fixture(autouse=True)
async def mock_mongo(container: MockContainer) -> AsyncGenerator[None, None]:
    mongo_client = container.mongo_client()
    db = mongo_client.synthesia_db
    await db.discussions.delete_many({})
    await db.notifications.delete_many({})
    await db.sessions.delete_many({})
    yield
