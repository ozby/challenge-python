from dataclasses import dataclass


@dataclass
class Reply:
    client_id: str
    comment: str


@dataclass
class Discussion:
    discussion_id: str
    reference_prefix: str
    time_marker: str
    client_id: str
    replies: list[Reply]
