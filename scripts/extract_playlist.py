#!/usr/bin/env python3
"""
extract_playlist.py

One-off utility that reads a YouTube playlist (via yt-dlp, no YouTube Data
API key required) and dumps an ordered list of videos into scripts/topics.json.

Usage:
    python scripts/extract_playlist.py "https://www.youtube.com/playlist?list=XXXXXXXX"

    # or run without arguments and paste the URL when prompted:
    python scripts/extract_playlist.py

The resulting scripts/topics.json has the schema:
    [
      {
        "day": 1,
        "slug": "day-01-horizontal-vs-vertical-scaling",
        "title": "Horizontal vs Vertical Scaling",
        "video_url": "https://www.youtube.com/watch?v=XXXXXXXXXXX"
      },
      ...
    ]

Existing topics.json (if any) is backed up to topics.json.bak before being
overwritten, so you never lose a hand-curated list by accident.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print(
        "ERROR: yt-dlp is not installed. Run `pip install -r requirements.txt` first.",
        file=sys.stderr,
    )
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
TOPICS_JSON_PATH = SCRIPT_DIR / "topics.json"


def slugify(title: str, day: int) -> str:
    """
    Convert a raw YouTube video title into a clean, filesystem-safe slug
    prefixed with a zero-padded day number, e.g.:

        "Horizontal vs Vertical Scaling | System Design #1"
        -> "day-01-horizontal-vs-vertical-scaling-system-design-1"
    """
    # Lowercase and strip
    slug = title.strip().lower()

    # Remove characters that aren't alphanumeric, space, or hyphen
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)

    # Collapse whitespace/hyphens into single hyphens
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")

    # Guard against an empty slug (e.g. title was all emoji/symbols)
    if not slug:
        slug = f"untitled-video-{day}"

    # Cap slug length so filenames stay sane
    max_len = 80
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit("-", 1)[0]

    return f"day-{day:02d}-{slug}"


def fetch_playlist_entries(playlist_url: str) -> list[dict]:
    """
    Use yt-dlp in 'flat playlist' mode to fetch video titles and URLs
    without downloading any media or requiring authentication.
    """
    ydl_opts = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    if info is None:
        raise RuntimeError("yt-dlp returned no data for this playlist URL.")

    entries = info.get("entries")
    if not entries:
        raise RuntimeError(
            "No videos found in playlist. Check that the URL is a public "
            "or unlisted playlist link."
        )

    return list(entries)


def build_topics(entries: list[dict]) -> list[dict]:
    topics = []
    day = 1

    for entry in entries:
        if entry is None:
            # yt-dlp can return None entries for deleted/private videos
            continue

        title = entry.get("title") or f"Untitled Video {day}"
        video_id = entry.get("id") or entry.get("url")

        if not video_id:
            continue

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        slug = slugify(title, day)

        topics.append(
            {
                "day": day,
                "slug": slug,
                "title": title,
                "video_url": video_url,
            }
        )
        day += 1

    return topics


def main() -> None:
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1].strip()
    else:
        playlist_url = input("Paste the YouTube playlist URL: ").strip()

    if not playlist_url:
        print("ERROR: No playlist URL provided.", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching playlist metadata from: {playlist_url}")
    entries = fetch_playlist_entries(playlist_url)
    topics = build_topics(entries)

    if not topics:
        print("ERROR: No usable videos were extracted from this playlist.", file=sys.stderr)
        sys.exit(1)

    if TOPICS_JSON_PATH.exists():
        backup_path = TOPICS_JSON_PATH.with_suffix(".json.bak")
        backup_path.write_text(TOPICS_JSON_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Existing topics.json backed up to {backup_path.name}")

    TOPICS_JSON_PATH.write_text(
        json.dumps(topics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"Wrote {len(topics)} topics to {TOPICS_JSON_PATH}")
    for t in topics[:5]:
        print(f"  day {t['day']:02d}: {t['slug']}")
    if len(topics) > 5:
        print(f"  ... and {len(topics) - 5} more")


if __name__ == "__main__":
    main()
