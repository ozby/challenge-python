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
            "db_name": "test_db",
        }
    )

    mongo_client = cast(
        providers.Provider[AsyncIOMotorClient[Any]],
        providers.Singleton(
            AsyncIOMotorClient,
            config.mongo_uri,
        ),
    )

    db = providers.Singleton(
        lambda client, db_name: client[db_name], mongo_client, config.db_name
    )

    notification_service = providers.Singleton(NotificationService, db)

    session_service = providers.Singleton(SessionService, db)

    discussion_service = providers.Singleton(
        DiscussionService,
        db,
        notification_service=notification_service,
    )
