from __future__ import annotations

from pathlib import Path

from youtube_news_agent.models import ScoredVideo


def render_digest(videos: list[ScoredVideo], limit: int = 10) -> str:
    top_videos = sorted(videos, key=lambda item: item.score, reverse=True)[:limit]

    lines = [
        "# YouTube News Digest",
        "",
        f"Top {len(top_videos)} videos ranked by simple quality heuristics.",
        "",
    ]

    for index, item in enumerate(top_videos, start=1):
        video = item.video
        reason_text = ", ".join(item.reasons) if item.reasons else "no special signals"
        lines.extend(
            [
                f"## {index}. {video.title}",
                "",
                f"- Channel: {video.channel}",
                f"- Published: {video.publish_date.date().isoformat()}",
                f"- Score: {item.score}",
                f"- URL: {video.url}",
                f"- Why it ranked: {reason_text}",
                "",
                video.description.strip() or "No description provided.",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def write_digest(path: str | Path, content: str) -> None:
    Path(path).write_text(content)
