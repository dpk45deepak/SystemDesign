# System Design in Hinglish 🇮🇳⚙️

![Daily Automation](https://img.shields.io/badge/automation-daily-brightgreen)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Hinglish Tech Notes](https://img.shields.io/badge/notes-Hinglish-orange)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

> Har din ek naya System Design concept — seedhe, apne andaaz mein. Bina jargon ke bojh ke.

## 🤔 Why this repo exists

Zyaadatar System Design content ya to bahut academic hai, ya phir itna dry hai ki
interview ke 2 din pehle yaad hi nahi rehta. Yeh repo ek fully automated engine hai
jo **roz ek naya System Design guide** generate karta hai — Swiggy, IRCTC, Zerodha
jaise Indian products ke relatable examples ke saath, clean Mermaid diagrams ke
saath, aur ek crisp interview cheat-sheet ke saath.

Koi manual likhne ka jhanjhat nahi. Ek GitHub Actions workflow roz subah 9 AM IST
pe chalta hai, agla topic uthata hai, Gemini se guide banata hai, aur khud commit
kar deta hai. Fork karo, apna playlist daalo, aur apna khud ka daily-updating
System Design notebook bana lo.

## 📚 Progress Tracker

| Day | Topic | Video Link | Notes | Status |
|-----|-------|------------|-------|--------|
| 1 | [Vertical vs Horizontal Scaling](topics/day-01-vertical-vs-horizontal-scaling.md) | [Watch](https://www.youtube.com/watch?v=xpDnVSmNFX0) | Sample guide, included out of the box | [x] |
| 2 | Load Balancers | [Watch](https://www.youtube.com/watch?v=K0Ta65OqQkY) | | [ ] |
| 3 | Caching Strategies | [Watch](https://www.youtube.com/watch?v=U3RkDLtS7uY) | | [ ] |
| 4 | Database Indexing | [Watch](https://www.youtube.com/watch?v=fsG1XaZEa78) | | [ ] |
| 5 | Database Sharding | [Watch](https://www.youtube.com/watch?v=v3Ehy1O0edA) | | [ ] |
| 6 | Consistent Hashing | [Watch](https://www.youtube.com/watch?v=zaRkONvyGr8) | | [ ] |
| 7 | CAP Theorem | [Watch](https://www.youtube.com/watch?v=BHqjEjzAicA) | | [ ] |

*This table is auto-updated by `scripts/generator.py` every time a new guide is published — the "Topic" cell becomes a link to the generated markdown file and the status flips to `[x]`.*

## 🗂️ Repository Structure

```
system-design-in-hinglish/
├── .github/
│   └── workflows/
│       └── daily-post.yml          # Daily cron job: generates + commits + pushes
├── scripts/
│   ├── extract_playlist.py         # One-off: YouTube playlist -> topics.json
│   ├── generator.py                # Main engine: Gemini call + file write + README update
│   └── topics.json                 # Ordered index of all topics/videos
├── topics/                         # Generated daily markdown guides land here
│   └── day-01-vertical-vs-horizontal-scaling.md
├── README.md
├── requirements.txt
└── .env.example
```

## 🚀 Running it locally

1. **Clone and install dependencies**

   ```bash
   git clone https://github.com/<your-username>/system-design-in-hinglish.git
   cd system-design-in-hinglish
   pip install -r requirements.txt
   ```

2. **Set up your API key**

   ```bash
   cp .env.example .env
   # then edit .env and add your GEMINI_API_KEY
   export $(cat .env | xargs)   # or use a tool like direnv / python-dotenv
   ```

   Get a free Gemini API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

3. **(Optional) Seed your own topic list from a YouTube playlist**

   ```bash
   python scripts/extract_playlist.py "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
   ```

   This overwrites `scripts/topics.json` with your playlist's videos, in order
   (a backup of the previous file is saved as `scripts/topics.json.bak`).

4. **Generate the next guide manually**

   ```bash
   python scripts/generator.py
   ```

   This finds the next topic without a markdown file, calls Gemini, writes
   `topics/{slug}.md`, and updates the progress table in this README.

## 🤖 How the automation works

- `.github/workflows/daily-post.yml` runs every day at **3:30 AM UTC (9:00 AM IST)**,
  and can also be triggered manually from the **Actions** tab (`workflow_dispatch`).
- It installs dependencies, runs `scripts/generator.py` (using the `GEMINI_API_KEY`
  repository secret), and if a new file was generated, commits and pushes it to
  `main` as `SystemDesign Bot <actions@github.com>`.
- If every topic in `topics.json` already has a generated file, the script exits
  cleanly without making any changes — so the workflow is always safe to run.

### Setting up the automation on your fork

1. Go to **Settings → Secrets and variables → Actions** on your fork.
2. Add a new repository secret named `GEMINI_API_KEY` with your Gemini API key.
3. That's it — the workflow will start running on the daily schedule, or you can
   trigger it immediately from **Actions → Daily System Design Post → Run workflow**.

## 🙌 Contributing

Contributions are welcome!

- **Add more topics**: open a PR adding entries to `scripts/topics.json`
  (or extend it via `extract_playlist.py` with a new playlist).
- **Improve the prompt**: tweak `build_prompt()` in `scripts/generator.py` to
  improve tone, structure, or add new sections.
- **Fix a generated guide**: generated markdown files in `topics/` are plain
  Markdown — feel free to open a PR editing them directly for accuracy or
  clarity.
- **Report issues**: found a broken diagram or a factual error? Open an issue.

Fork the repo, make your changes, and submit a pull request. Please keep the
Hinglish tone consistent with the existing guides.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
