from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen
from xml.etree import ElementTree

from youtube_news_agent.models import ChannelConfig, Video

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
MEDIA_NS = {"media": "http://search.yahoo.com/mrss/"}


def build_feed_url(channel: ChannelConfig) -> str:
    if channel.feed_url:
        return channel.feed_url

    assert channel.channel_id is not None
    query = urlencode({"channel_id": channel.channel_id})
    return f"https://www.youtube.com/feeds/videos.xml?{query}"


def fetch_recent_videos(channel: ChannelConfig, limit: int = 5) -> list[Video]:
    feed_url = build_feed_url(channel)
    with urlopen(feed_url, timeout=20) as response:
        payload = response.read()

    root = ElementTree.fromstring(payload)
    videos: list[Video] = []

    for entry in root.findall("atom:entry", ATOM_NS)[:limit]:
        title = _text(entry, "atom:title", ATOM_NS)
        video_url = _text(entry, "atom:link", ATOM_NS, attribute="href")
        published = _text(entry, "atom:published", ATOM_NS)
        description = _text(entry, "media:group/media:description", MEDIA_NS)

        videos.append(
            Video(
                title=title,
                channel=channel.name,
                publish_date=_parse_datetime(published),
                description=description,
                url=video_url,
            )
        )

    return videos


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(
        timezone.utc
    )


def _text(
    element: ElementTree.Element,
    path: str,
    namespace: dict[str, str],
    attribute: Optional[str] = None,
) -> str:
    child = element.find(path, namespace)
    if child is None:
        return ""
    if attribute:
        return child.attrib.get(attribute, "")
    return child.text or ""
