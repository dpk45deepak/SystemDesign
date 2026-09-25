# System Design in Hinglish 🇮🇳⚙️

![Daily Automation](https://img.shields.io/badge/automation-daily-brightgreen)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Hinglish Tech Notes](https://img.shields.io/badge/notes-Hinglish-orange)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

> Har din ek naya System Design concept — seedhe, apne andaaz mein. Bina jargon ke bojh ke.

## 🗂️ Repository Structure

```
system-design-in-hinglish/
├── .github/
│   └── workflows/
│       └── daily-post.yml          # Daily cron job: generates + commits + pushes
├── scripts/
│   ├── extract_playlist.py         # One-off: YouTube playlist -> topics.json
│   ├── generator.py                # Main engine: Groq call + file write + README update
│   └── topics.json                 # Ordered index of all topics/videos
├── topics/                         # Generated daily markdown guides land here
│   └── day-01-vertical-vs-horizontal-scaling.md
├── README.md
├── requirements.txt
└── .env.example
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
