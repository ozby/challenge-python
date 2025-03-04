import logging
from datetime import datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from server.entities.notification import Notification, NotificationType


class NotificationService:
    def __init__(self, db: AsyncIOMotorDatabase[Any]) -> None:
        self.db = db
        self.notifications = self.db.notifications

    async def create_reply_notifications(
        self, discussion_id: str, sender_id: str, recipient_ids: list[str]
    ) -> None:
        """Create reply notifications for all recipients except the sender"""
        if not recipient_ids:
            return

        notifications = [
            {
                "discussion_id": discussion_id,
                "recipient_id": recipient_id,
                "sender_id": sender_id,
                "notification_type": NotificationType.REPLY.value,
                "created_at": datetime.now(),
            }
            for recipient_id in recipient_ids
            if recipient_id != sender_id  # Don't notify the sender
        ]

        if notifications:
            await self.notifications.insert_many(notifications)
            logging.info(
                f"Created {len(notifications)} reply notifications for discussion {discussion_id}"
            )

    async def create_mention_notifications(
        self, discussion_id: str, sender_id: str, mentioned_ids: list[str]
    ) -> None:
        """Create mention notifications for all mentioned users except the sender"""
        if not mentioned_ids:
            return

        notifications = [
            {
                "discussion_id": discussion_id,
                "recipient_id": recipient_id,
                "sender_id": sender_id,
                "notification_type": NotificationType.MENTION.value,
                "created_at": datetime.now(),
            }
            for recipient_id in mentioned_ids
            if recipient_id != sender_id
        ]

        if notifications:
            await self.notifications.insert_many(notifications)
            logging.info(
                f"Created {len(notifications)} mention notifications for discussion {discussion_id}"
            )

    async def get_notifications(self, recipient_id: str) -> list[Notification]:
        """Get all notifications for a recipient"""
        notification_docs = (
            await self.notifications.find({"recipient_id": recipient_id}, {"_id": 0})
            .sort("created_at", -1)
            .to_list(length=None)
        )

        return [
            Notification(
                **{
                    **doc,
                    "notification_type": NotificationType(doc["notification_type"]),
                }
            )
            for doc in notification_docs
        ]

    async def mark_as_read(self, recipient_id: str, discussion_id: str) -> None:
        """Mark notifications as read for a specific discussion"""
        await self.notifications.delete_many(
            {"recipient_id": recipient_id, "discussion_id": discussion_id}
        )
