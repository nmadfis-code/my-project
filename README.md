# YouTube News Agent

[![Python Tests](https://github.com/nmadfis-code/my-project/actions/workflows/python-tests.yml/badge.svg)](https://github.com/nmadfis-code/my-project/actions/workflows/python-tests.yml)

A small Python project that reads YouTube channels from `channels.yaml`, fetches recent videos, scores them with simple heuristics, and writes a markdown digest of the top 10 videos.

## Features

- Loads channels from `channels.yaml`
- Fetches recent uploads from YouTube channel feeds
- Stores title, channel, publish date, description, and URL
- Scores videos with readable rule-based heuristics
- Writes a markdown digest to `digest.md`
- Includes pytest tests for scoring

## Project Layout

```text
youtube_news_agent/
  config.py
  digest.py
  models.py
  scoring.py
  youtube.py
  main.py
tests/
channels.yaml
pyproject.toml
README.md
```

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .[dev]
```

## Configure Channels

Edit `channels.yaml` and add the channels you want to track.

Each entry should include a human-friendly name and a YouTube channel ID:

```yaml
channels:
  - name: Example News
    channel_id: UC1234567890ABCDEFGHIJ
```

You can also provide a custom feed URL:

```yaml
channels:
  - name: Example News
    feed_url: https://www.youtube.com/feeds/videos.xml?channel_id=UC1234567890ABCDEFGHIJ
```

## Usage

Run the agent:

```bash
python -m youtube_news_agent
```

By default it writes the markdown digest to `digest.md`.

You can choose a different output path:

```bash
python -m youtube_news_agent --output reports/today.md
```

## Run Tests

```bash
pytest
```

## Notes

- This project uses YouTube's public channel feed endpoint and avoids extra API setup.
- The scoring rules are intentionally simple so they are easy to change.
- If a channel feed cannot be fetched, the program skips it and keeps going.
