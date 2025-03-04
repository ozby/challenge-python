import logging
from datetime import datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from server.entities.session import Session


class SessionService:
    def __init__(self, db: AsyncIOMotorDatabase[Any]) -> None:
        self.sessions = db.sessions

    async def set(self, peer_id: str, user_id: str) -> None:
        logging.info(f"Setting session for {peer_id} to {user_id}")
        session_doc = {
            "peer_id": peer_id,
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        await self.sessions.update_one(
            {"peer_id": peer_id}, {"$set": session_doc}, upsert=True
        )

    async def get_client_id(self, peer_id: str | None) -> str | None:
        if peer_id is None:
            return None
        session_doc = await self.sessions.find_one({"peer_id": peer_id}, {"_id": 0})
        if not session_doc:
            return None
        session = Session(**session_doc)
        return session.user_id

    async def get_by_user_id(self, user_id: str | None) -> str | None:
        if user_id is None:
            return None
        session_doc = await self.sessions.find_one({"user_id": user_id}, {"_id": 0})
        if not session_doc:
            return None
        session = Session(**session_doc)
        return session.peer_id

    async def get_session(self, peer_id: str | None) -> Session | None:
        if peer_id is None:
            return None
        session_doc = await self.sessions.find_one({"peer_id": peer_id}, {"_id": 0})
        if not session_doc:
            return None
        return Session(**session_doc)

    async def delete(self, peer_id: str | None) -> None:
        if peer_id is not None:
            await self.sessions.delete_one({"peer_id": peer_id})
