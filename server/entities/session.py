from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    peer_id: str
    user_id: str
    created_at: datetime
