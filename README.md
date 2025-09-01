
# automation-samples

A ready-to-publish starter repo with small, **real** automation examples you can run locally or via **GitHub Actions**. Use this as a portfolio to show practical automation skills.

## What's inside
- **scripts/url_check.py** – checks a list of URLs and writes a CSV uptime report
- **scripts/slack_webhook.py** – posts messages to Slack/Discord-compatible webhooks
- **samples/csv_deduper.py** – removes duplicate rows from a CSV by key column
- **samples/bulk_rename.py** – bulk-renames files with a pattern
- **samples/json_to_csv.py** – converts a JSONL (or JSON array) to CSV
- **.github/workflows/url-uptime.yml** – scheduled uptime checks + artifacts
- **.github/workflows/notify-on-failure.yml** – sends Slack webhook alert if uptime job fails

All examples use only Python **standard library** (no external dependencies).

## Quick start (local)
```bash
# 1) Clone or download this repo
# 2) Create a virtual env (optional)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Copy config and fill in
cp .env.example .env

# 4) Add URLs to check
echo "https://example.com" > urls.txt
echo "https://httpstat.us/503" >> urls.txt

# 5) Run a sample
python scripts/url_check.py --input urls.txt --out reports/uptime.csv --retries 1 --timeout 8
python scripts/slack_webhook.py --text "Hello from automation-samples!" --webhook "$SLACK_WEBHOOK_URL"
```

## Run on GitHub Actions (recommended for your portfolio)
1. Create a new public repo on GitHub named `automation-samples`.
2. Push this project (see the **Publish to GitHub** section below).
3. In **Settings → Secrets and variables → Actions → New repository secret**, add:
   - `SLACK_WEBHOOK_URL` – your Slack/Discord Incoming Webhook (optional, for alerts).
4. Commit any change and go to **Actions**. Enable workflows if prompted.
5. The **Uptime Check** workflow will run on a schedule and on every push. See artifacts.

### Customize
- Edit `urls.txt` to monitor any sites (your landing pages, API endpoints, etc.).
- Tweak CRON in `.github/workflows/url-uptime.yml`.
- Replace Slack with Discord (webhook is compatible).

## Publish to GitHub
```bash
git init
git add .
git commit -m "feat: automation-samples starter"
git branch -M main
git remote add origin https://github.com/<your-username>/automation-samples.git
git push -u origin main
```

## Portfolio ideas
- Add a **README badge** with latest uptime status (use GitHub Actions artifacts or a gist).
- Record a short GIF showing `url_check.py` running and include it in README.
- Add more folders: `/google-sheets/`, `/email/`, `/integrations/*`.

## Structure
```
automation-samples/
├─ .github/
│  └─ workflows/
│     ├─ url-uptime.yml
│     └─ notify-on-failure.yml
├─ scripts/
│  ├─ url_check.py
│  └─ slack_webhook.py
├─ samples/
│  ├─ csv_deduper.py
│  ├─ bulk_rename.py
│  └─ json_to_csv.py
├─ urls.txt
├─ .env.example
├─ LICENSE
├─ .gitignore
└─ README.md
```

## Notes
- Keep secrets out of the repo. Use `.env` locally and **GitHub Secrets** in Actions.
- All code here aims to be simple and readable for clients to vet quickly.
