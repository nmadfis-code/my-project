from __future__ import annotations

import argparse
from pathlib import Path

from youtube_news_agent.config import load_channels
from youtube_news_agent.digest import render_digest, write_digest
from youtube_news_agent.scoring import score_video
from youtube_news_agent.youtube import fetch_recent_videos


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a YouTube news markdown digest.")
    parser.add_argument(
        "--channels",
        default="channels.yaml",
        help="Path to the channels YAML file.",
    )
    parser.add_argument(
        "--output",
        default="digest.md",
        help="Where to write the markdown digest.",
    )
    parser.add_argument(
        "--per-channel",
        type=int,
        default=5,
        help="How many recent videos to fetch per channel.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    channels = load_channels(args.channels)

    scored_videos = []
    for channel in channels:
        try:
            videos = fetch_recent_videos(channel, limit=args.per_channel)
        except Exception as exc:
            print(f"Skipping {channel.name}: {exc}")
            continue

        scored_videos.extend(score_video(video) for video in videos)

    digest = render_digest(scored_videos, limit=10)
    write_digest(Path(args.output), digest)
    print(f"Wrote digest to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
