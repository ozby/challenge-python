import random
import re
import string
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from server.entities.discussion import Discussion, Reply
from server.services.notification_service import NotificationService


class DiscussionService:
    MENTION_PATTERN = re.compile(r"(?<!@)@(\w+)(?=[\s,.!?]|$)")

    def __init__(
        self,
        mongo_client: AsyncIOMotorClient[Any],
        notification_service: NotificationService,
    ) -> None:
        self.db = mongo_client.synthesia_db
        self.discussions = self.db.discussions
        self.notification_service = notification_service

    def _sanitize_comment(self, comment: str) -> str:
        if "," in comment:
            escaped_comment = comment.replace('"', '""')
            return f'"{escaped_comment}"'
        return comment

    def _get_unique_participants(self, discussion_doc: dict[str, Any]) -> set[str]:
        """Get unique client_ids from a discussion's replies"""
        participants = {discussion_doc["client_id"]}
        for reply in discussion_doc["replies"]:
            participants.add(reply["client_id"])
        return participants

    def _extract_mentions(self, comment: str) -> set[str]:
        """Extract mentioned client_ids from a comment"""
        return set(self.MENTION_PATTERN.findall(comment))

    async def create_discussion(
        self, reference: str, comment: str, client_id: str
    ) -> str:
        reference_prefix = reference.split(".")[0]
        discussion_id = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=7)
        )

        discussion_doc = {
            "discussion_id": discussion_id,
            "reference_prefix": reference_prefix,
            "reference": reference,
            "client_id": client_id,
            "replies": [
                {"client_id": client_id, "comment": self._sanitize_comment(comment)}
            ],
        }

        await self.discussions.insert_one(discussion_doc)

        mentioned_users = self._extract_mentions(comment)
        if mentioned_users:
            await self.notification_service.create_mention_notifications(
                discussion_id=discussion_id,
                sender_id=client_id,
                mentioned_ids=list(mentioned_users),
            )

        return discussion_id

    async def create_reply(
        self, discussion_id: str, comment: str, client_id: str
    ) -> str:
        discussion_doc = await self.discussions.find_one(
            {"discussion_id": discussion_id}, {"_id": 0}
        )
        if not discussion_doc:
            raise ValueError(f"Discussion {discussion_id} not found")

        participants = self._get_unique_participants(discussion_doc) - {client_id}

        new_reply = {"client_id": client_id, "comment": self._sanitize_comment(comment)}
        await self.discussions.update_one(
            {"discussion_id": discussion_id}, {"$push": {"replies": new_reply}}
        )

        await self.notification_service.create_reply_notifications(
            discussion_id=discussion_id,
            sender_id=client_id,
            recipient_ids=list(participants),
        )

        mentioned_users = self._extract_mentions(comment)
        if mentioned_users:
            await self.notification_service.create_mention_notifications(
                discussion_id=discussion_id,
                sender_id=client_id,
                mentioned_ids=list(mentioned_users),
            )

        return discussion_id

    async def get_discussion(self, discussion_id: str) -> Discussion:
        discussion_doc = await self.discussions.find_one(
            {"discussion_id": discussion_id}, {"_id": 0}
        )
        if not discussion_doc:
            raise ValueError(f"Discussion {discussion_id} not found")

        return Discussion(
            discussion_id=discussion_doc["discussion_id"],
            reference_prefix=discussion_doc["reference_prefix"],
            reference=discussion_doc["reference"],
            client_id=discussion_doc["client_id"],
            replies=[Reply(**reply) for reply in discussion_doc["replies"]],
        )

    async def list_discussions(
        self, reference_prefix: str | None = None
    ) -> list[Discussion]:
        query = {"reference_prefix": reference_prefix} if reference_prefix else {}
        discussion_docs = await self.discussions.find(query, {"_id": 0}).to_list(
            length=None
        )

        return [
            Discussion(
                discussion_id=doc["discussion_id"],
                reference_prefix=doc["reference_prefix"],
                reference=doc["reference"],
                client_id=doc["client_id"],
                replies=[Reply(**reply) for reply in doc["replies"]],
            )
            for doc in discussion_docs
        ]

    async def delete_discussion(self, discussion_id: str) -> None:
        await self.discussions.delete_one({"discussion_id": discussion_id})

    async def delete_reply(self, discussion_id: str, reply_id: str) -> None:
        pass
