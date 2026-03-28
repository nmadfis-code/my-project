from datetime import datetime, timedelta, timezone

from youtube_news_agent.models import Video
from youtube_news_agent.scoring import score_video


def make_video(
    *,
    title: str = "Deep analysis of policy changes",
    description: str = "A detailed report on major policy shifts and market effects." * 5,
    hours_ago: int = 6,
) -> Video:
    now = datetime(2026, 3, 27, 12, 0, tzinfo=timezone.utc)
    return Video(
        title=title,
        channel="Test Channel",
        publish_date=now - timedelta(hours=hours_ago),
        description=description,
        url="https://youtube.com/watch?v=test",
    )


def test_recent_analytical_video_scores_well() -> None:
    now = datetime(2026, 3, 27, 12, 0, tzinfo=timezone.utc)
    result = score_video(make_video(), now=now)

    assert result.score >= 8.0
    assert "published within the last day" in result.reasons
    assert "title suggests timely or analytical coverage" in result.reasons


def test_old_short_clip_scores_lower() -> None:
    now = datetime(2026, 3, 27, 12, 0, tzinfo=timezone.utc)
    old_clip = make_video(
        title="Short clip",
        description="brief",
        hours_ago=200,
    )

    result = score_video(old_clip, now=now)

    assert result.score <= -1.5
    assert "title looks more like a short clip than a full report" in result.reasons
    assert "title is very short" in result.reasons


def test_longer_description_gets_bonus() -> None:
    now = datetime(2026, 3, 27, 12, 0, tzinfo=timezone.utc)
    short_description_video = make_video(description="Short summary only.")
    long_description_video = make_video(
        description="Detailed context about war, policy, and market reactions. " * 10
    )

    short_result = score_video(short_description_video, now=now)
    long_result = score_video(long_description_video, now=now)

    assert long_result.score > short_result.score
    assert "description includes useful context" in long_result.reasons
