from typing import Any

from mongomock_motor import AsyncMongoMockClient  # type: ignore
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class AsyncMongoClient:
    def __init__(self) -> None:
        self.client: (
            AsyncMongoMockClient[dict[str, Any]] | AsyncIOMotorClient[dict[str, Any]]
        )
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db: AsyncIOMotorDatabase[dict[str, Any]] = self.client.synthesia_db

    def close(self) -> None:
        """Close the MongoDB connection"""
        self.client.close()


async_mongo_client = AsyncMongoClient()
