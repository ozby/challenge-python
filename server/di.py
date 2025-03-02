"""Dependency injection setup for the server."""

from typing import Any, cast

from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

from server.services.discussion_service import DiscussionService
from server.services.notification_service import NotificationService
from server.services.session_service import SessionService


class Container(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration(
        default={
            "mongo_uri": "mongodb://localhost:27017",
            "db_name": "synthesia_db",
        }
    )

    mongo_client = cast(
        providers.Provider[AsyncIOMotorClient[Any]],
        providers.Singleton(
            AsyncIOMotorClient,
            config.mongo_uri,
        ),
    )

    notification_service = providers.Singleton(
        NotificationService, mongo_client=mongo_client
    )

    session_service = providers.Singleton(SessionService, mongo_client=mongo_client)

    discussion_service = providers.Singleton(
        DiscussionService,
        mongo_client=mongo_client,
        notification_service=notification_service,
    )
