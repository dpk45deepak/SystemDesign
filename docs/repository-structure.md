# Repository Structure and File Locations

This repository is organized for a daily system-design learning workflow with automation, scripts, and generated topic notes.

## Top-level files

- `README.md` — project overview, repository structure, and project description.
- `LICENSE` — MIT license for the repository.
- `.gitignore` — ignores local environment files and generated artifacts.
- `.env.example` — sample environment configuration for API keys and runtime settings.
- `requirements.txt` — Python dependencies required by the automation scripts.

## GitHub automation

- `.github/workflows/` — GitHub Actions automation files.
  - `.github/workflows/daily-post.yml` — scheduled workflow that generates and publishes daily topic content.

## Script directory

- `scripts/` — automation and generation logic.
  - `scripts/generator.py` — primary script that creates the daily content and updates the repo.
  - `scripts/extract_playlist.py` — helper script to convert playlist information into `topics.json`.
  - `scripts/topics.json` — ordered topic index used by the generator.

## Topic content directory

- `topics/` — generated topic markdown files.
  - `topics/day-01-how-to-design-apis-like-a-senior-engineer-rest-graphql-auth-security.md`
  - `topics/day-02-api-security-explained-rate-limiting-cors-sql-injection-csrf-xss-more.md`
  - `topics/day-03-authentication-explained-when-to-use-basic-bearer-oauth2-jwt-sso.md`
  - `topics/day-04-7-authentication-concepts-every-developer-should-know.md`
  - `topics/day-05-api-protocols-explained-when-to-use-http-websockets-grpc-more.md`
  - `topics/day-06-api-design-101-from-basics-to-best-practices.md`
  - `topics/day-07-database-replication-sharding-explained.md`
  - `topics/day-08-how-to-scale-like-a-senior-engineer-servers-dbs-lbs-spofs.md`
  - `topics/day-09-stateful-vs-stateless-architectures-explained.md`
  - `topics/day-10-message-queues-in-system-design.md`
  - `topics/day-11-rest-api-basics-best-practices-explained.md`
  - `topics/day-12-6-system-design-interview-concepts.md`
  - `topics/day-13-system-design-interview-mastering-databases.md`
  - `topics/day-14-object-storage-blobs-explained-for-system-design.md`
  - `topics/day-15-map-reduce-explained-with-example-system-design.md`
  - `topics/day-16-system-design-concepts-architecture-of-production-web-apps.md`
  - `topics/day-17-api-design-101-from-basics-to-best-practices.md`

## Repository flow

The repository follows a simple structure:

```text
SystemDesign/
├── .env.example
├── .github/
│   └── workflows/
│       └── daily-post.yml
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── scripts/
│   ├── extract_playlist.py
│   ├── generator.py
│   └── topics.json
├── topics/
│   ├── day-01-...
│   ├── day-02-...
│   └── ...
└── docs/
    └── repository-structure.md
```

This layout keeps configuration, automation, code generation logic, and produced study content separated for clarity and maintainability.
