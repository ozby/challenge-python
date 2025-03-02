from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class NotificationType(Enum):
    REPLY = "reply"
    MENTION = "mention"


@dataclass
class Notification:
    discussion_id: str
    recipient_id: str
    sender_id: str
    notification_type: NotificationType
    created_at: datetime
