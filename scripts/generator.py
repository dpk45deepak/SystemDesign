#!/usr/bin/env python3
"""
generator.py

Main daily engine for system-design-in-hinglish.

What it does, in order:
  1. Loads scripts/topics.json (the ordered topic index).
  2. Finds the first topic whose markdown file does not yet exist inside
     topics/.
  3. Calls the Gemini API (via google-genai) with a strict formatting
     prompt to generate a high-retention, Hinglish system design guide.
  4. Writes the result to topics/{slug}.md.
  5. Parses README.md and flips that topic's row in the progress tracker
     table from "[ ]" to "[x]", linking to the new file.

Designed to be run once a day (see .github/workflows/daily-post.yml), but
is fully safe to run manually / repeatedly: if every topic already has a
file, it exits cleanly without calling the API.

Environment variables (see .env.example):
    GEMINI_API_KEY   - required, your Gemini API key
    GEMINI_MODEL     - optional, defaults to "gemini-2.5-flash"
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types as genai_types
except ImportError:
    print(
        "ERROR: google-genai is not installed. Run `pip install -r requirements.txt` first.",
        file=sys.stderr,
    )
    sys.exit(1)

# --------------------------------------------------------------------------
# Paths / config
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_JSON_PATH = Path(os.environ.get("TOPICS_JSON_PATH", REPO_ROOT / "scripts" / "topics.json"))
TOPICS_OUTPUT_DIR = Path(os.environ.get("TOPICS_OUTPUT_DIR", REPO_ROOT / "topics"))
README_PATH = Path(os.environ.get("README_PATH", REPO_ROOT / "README.md"))

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Markers that must exist in README.md so we know where to look for the
# progress table. See README.md for the actual table.
README_TABLE_ROW_PATTERN = re.compile(
    r"^\|\s*{day}\s*\|(?P<rest>.*)\|\s*\[\s\]\s*\|\s*$"
)


# --------------------------------------------------------------------------
# Step 1: load topics.json
# --------------------------------------------------------------------------

def load_topics() -> list[dict]:
    if not TOPICS_JSON_PATH.exists():
        print(f"ERROR: {TOPICS_JSON_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    with open(TOPICS_JSON_PATH, "r", encoding="utf-8") as f:
        topics = json.load(f)

    if not isinstance(topics, list) or not topics:
        print("ERROR: topics.json is empty or malformed.", file=sys.stderr)
        sys.exit(1)

    # Keep them in day order regardless of how they're stored on disk
    topics.sort(key=lambda t: t["day"])
    return topics


# --------------------------------------------------------------------------
# Step 2: find next topic without a markdown file
# --------------------------------------------------------------------------

def find_next_topic(topics: list[dict]) -> dict | None:
    TOPICS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for topic in topics:
        md_path = TOPICS_OUTPUT_DIR / f"{topic['slug']}.md"
        if not md_path.exists():
            return topic
    return None


# --------------------------------------------------------------------------
# Step 3: build the Gemini prompt and call the API
# --------------------------------------------------------------------------

def build_prompt(topic: dict) -> str:
    return f"""Tum ek senior staff-level Software Architect aur ek zabardast Hinglish tech
content writer ho, jo Indian software engineers ke liye System Design sikhate ho.

Tumhe ek pura Markdown guide likhna hai is topic par:

Topic: {topic['title']}
Reference video: {topic['video_url']}

STRICT OUTPUT RULES:
- Pura output valid GitHub-flavored Markdown hona chahiye. Koi extra commentary,
  koi "Here is your markdown" jaisi cheez mat likho. Seedha Markdown se shuru karo.
- Tone: natural, conversational Hinglish (jaise ek senior engineer apne junior ko
  samjha raha ho). Engineering terms (Latency, Throughput, Read Replica, Gossip
  Protocol, Consistency, Availability, Load Balancer, etc.) ko English mein hi
  rakho, baaki sentence construction Hindi-English mix mein ho.
- Analogies India-centric aur relatable rakho: Swiggy, Zomato, IRCTC, Zerodha,
  Paytm, Ola/Uber jaise examples use karo jahan relevant ho.

Guide ka EXACT structure yeh hona chahiye (yeh headings hooby-hoo follow karo):

# {topic['title']}

> Video Reference: [{topic['title']}]({topic['video_url']})

## 1. Asli Problem Kya Hai? (The Core Why)
Ek relatable, high-traffic Indian product (Swiggy, IRCTC, Zerodha, etc.) ka
real example lekar samjhao ki yeh problem kyun exist karti hai aur agar isse
solve na kiya jaye to kya dikkat aati hai.

## 2. Core Architecture & Mechanisms
Is concept ke andar ka kaam-kaaj deeply samjhao. Engineering terms English mein
rakho lekin unki intuition Hinglish mein explain karo. Zaroorat ho to sub-headings
(###) use karo.

## 3. Architecture Flow
Ek valid, clean ```mermaid code block do jo is concept ka architecture/flow
diagram dikhaye (graph TD ya sequenceDiagram, jo bhi sabse zyada sense banaye).
Diagram simple aur readable rakho, zyada nodes mat thoodo.

## 4. Production Case Study
Ek real duniya ki company (Uber, Netflix, WhatsApp, Amazon, etc.) kaise is
concept ko production mein use/solve karti hai, uska concrete example do.

## 5. Trade-offs (Pros vs Cons)
Ek clean Markdown table do do columns ke saath: "Pros" aur "Cons".

## 6. System Design Interview Cheat Sheet
5 crisp bullet points do jo interview mein turant yaad rakhne layak ho.

Ab upar diye gaye structure ko EXACTLY follow karte hue pura guide likho.
"""


def call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=genai_types.GenerateContentConfig(
            temperature=0.8,
            max_output_tokens=8192,
        ),
    )

    text = (response.text or "").strip()

    # Strip accidental ```markdown fences if the model wraps the whole thing
    if text.startswith("```"):
        text = re.sub(r"^```(?:markdown)?\s*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)

    if not text:
        print("ERROR: Gemini returned an empty response.", file=sys.stderr)
        sys.exit(1)

    return text


# --------------------------------------------------------------------------
# Step 4: write the markdown file
# --------------------------------------------------------------------------

def write_topic_file(topic: dict, content: str) -> Path:
    TOPICS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    md_path = TOPICS_OUTPUT_DIR / f"{topic['slug']}.md"
    md_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {md_path}")
    return md_path


# --------------------------------------------------------------------------
# Step 5: update README.md progress table
# --------------------------------------------------------------------------

def update_readme(topic: dict) -> None:
    if not README_PATH.exists():
        print(f"WARNING: {README_PATH} not found, skipping README update.", file=sys.stderr)
        return

    readme_text = README_PATH.read_text(encoding="utf-8")
    day_str = str(topic["day"])
    relative_link = f"topics/{topic['slug']}.md"

    lines = readme_text.splitlines()
    updated = False

    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue

        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue

        # First cell must match this topic's day number exactly
        if cells[0] != day_str:
            continue

        # Only touch rows that are still pending ("[ ]")
        if "[ ]" not in cells[-1]:
            continue

        # Columns: Day | Topic | Video Link | Notes | Status
        topic_cell = f"[{topic['title']}]({relative_link})"
        cells[1] = topic_cell
        cells[-1] = cells[-1].replace("[ ]", "[x]")

        lines[i] = "| " + " | ".join(cells) + " |"
        updated = True
        break

    if not updated:
        print(
            f"WARNING: Could not find a pending row for day {day_str} in README.md. "
            "README left unchanged.",
            file=sys.stderr,
        )
        return

    README_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated README.md: marked day {day_str} ({topic['title']}) as complete.")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    topics = load_topics()
    next_topic = find_next_topic(topics)

    if next_topic is None:
        print("All topics already have generated markdown files. Nothing to do.")
        return

    print(f"Next topic: day {next_topic['day']:02d} - {next_topic['title']}")

    prompt = build_prompt(next_topic)
    print("Calling Gemini API...")
    content = call_gemini(prompt)

    write_topic_file(next_topic, content)
    update_readme(next_topic)

    print("Done.")


if __name__ == "__main__":
    main()
