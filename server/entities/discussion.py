from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reply:
    client_id: str
    comment: str
    created_at: datetime


@dataclass
class Discussion:
    discussion_id: str
    reference_prefix: str
    time_marker: str
    client_id: str
    created_at: datetime
    replies: list[Reply]
