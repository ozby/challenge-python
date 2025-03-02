from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class AsyncMongoClient:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient[dict[str, Any]] = AsyncIOMotorClient(
            "mongodb://localhost:27017"
        )
        self.db: AsyncIOMotorDatabase[dict[str, Any]] = self.client.synthesia_db

    def close(self) -> None:
        """Close the MongoDB connection"""
        self.client.close()


async_mongo_client = AsyncMongoClient()
