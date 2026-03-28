from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from youtube_news_agent.models import ScoredVideo, Video

GOOD_KEYWORDS = {
    "breaking",
    "analysis",
    "explainer",
    "interview",
    "live",
    "report",
    "update",
}

LOW_SIGNAL_KEYWORDS = {
    "shorts",
    "short",
    "clip",
    "highlights",
    "reaction",
}


def score_video(video: Video, now: Optional[datetime] = None) -> ScoredVideo:
    now = now or datetime.now(timezone.utc)
    score = 0.0
    reasons: list[str] = []

    age_hours = (now - video.publish_date).total_seconds() / 3600
    if age_hours <= 24:
        score += 4.0
        reasons.append("published within the last day")
    elif age_hours <= 72:
        score += 2.5
        reasons.append("published within the last three days")
    elif age_hours <= 168:
        score += 1.0
        reasons.append("published within the last week")

    title_lower = video.title.lower()
    description_lower = video.description.lower()
    combined_text = f"{title_lower} {description_lower}"

    if any(keyword in title_lower for keyword in GOOD_KEYWORDS):
        score += 2.5
        reasons.append("title suggests timely or analytical coverage")

    if any(keyword in combined_text for keyword in {"election", "policy", "market", "war"}):
        score += 1.5
        reasons.append("content appears tied to a major news topic")

    description_length = len(video.description.strip())
    if description_length >= 200:
        score += 1.5
        reasons.append("description includes useful context")
    elif description_length >= 80:
        score += 0.75
        reasons.append("description has some context")

    if any(keyword in title_lower for keyword in LOW_SIGNAL_KEYWORDS):
        score -= 2.0
        reasons.append("title looks more like a short clip than a full report")

    if len(video.title.strip()) < 20:
        score -= 0.5
        reasons.append("title is very short")

    return ScoredVideo(video=video, score=round(score, 2), reasons=reasons)
