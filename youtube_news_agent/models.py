from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ChannelConfig:
    name: str
    channel_id: Optional[str] = None
    feed_url: Optional[str] = None


@dataclass(frozen=True)
class Video:
    title: str
    channel: str
    publish_date: datetime
    description: str
    url: str


@dataclass(frozen=True)
class ScoredVideo:
    video: Video
    score: float
    reasons: list[str]
