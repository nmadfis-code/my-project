from __future__ import annotations

from pathlib import Path

import yaml

from youtube_news_agent.models import ChannelConfig


def load_channels(path: str | Path) -> list[ChannelConfig]:
    raw_config = yaml.safe_load(Path(path).read_text()) or {}
    raw_channels = raw_config.get("channels", [])

    channels: list[ChannelConfig] = []
    for item in raw_channels:
        name = (item.get("name") or "").strip()
        channel_id = (item.get("channel_id") or "").strip() or None
        feed_url = (item.get("feed_url") or "").strip() or None

        if not name:
            raise ValueError("Each channel must include a name.")
        if not channel_id and not feed_url:
            raise ValueError(
                f"Channel '{name}' must include either channel_id or feed_url."
            )

        channels.append(
            ChannelConfig(
                name=name,
                channel_id=channel_id,
                feed_url=feed_url,
            )
        )

    return channels
