# Intelligence Hub

A Streamlit app that uses Claude + web search to produce real-time intelligence —
on-demand trend briefs and an automated daily marketing digest. Deployed at
[pulseagent.streamlit.app](https://pulseagent.streamlit.app).

Everything runs on Claude's built-in `web_search` tool (Claude searches the web
directly and returns a structured markdown brief). There are no scrapers, RSS
parsers, or third-party automation/email services.

## Features

### Trend Brief
Enter any topic and get a structured brief — top story, narrative threads, a
sentiment snapshot, an emerging signal, "so what", and resources — synthesized
from live web search.

### Daily Marketing Digest
A once-a-day roundup of what a curated set of publications covered in the last
24–48 hours, across five areas:

- **Marketing & Advertising** — Marketing Brew, Ad Age, Marketing Dive, The Drum
- **Digital Marketing** — MarTech, Search Engine Land, Digiday
- **Branding & Brand Intelligence** — Branding Strategy Insider, WARC, Brandwatch
- **Social Media** — Social Media Today, Sprout Social Insights

Each category gets a short bulleted section, followed by a **Cross-Source
Themes** section flagging where multiple sources are converging. The source list
lives in `DIGEST_SOURCES` in `digest.py` — swap publications in or out there and
the prompt updates automatically; no other code changes needed.

You can preview the digest in the app via the **Daily Digest** button in the
sidebar, or have it emailed automatically each morning.

## Layout

| File | Purpose |
| --- | --- |
| `streamlit_app.py` | Streamlit UI (trend brief + digest preview). `app.py` is a deploy-time mirror. |
| `digest.py` | `DIGEST_SOURCES` and `run_daily_digest()` |
| `mailer.py` | `send_email()` — stdlib `smtplib` over SSL |
| `shared.py` | Shared client/model config and the markdown→HTML helper |
| `scripts/run_digest_and_email.py` | Headless entry point: build digest + email it |
| `.github/workflows/daily-digest.yml` | Daily cron that runs the script |

## Daily email schedule

The digest is sent by the `daily-digest.yml` GitHub Actions workflow.

> **Note:** GitHub Actions cron runs in **UTC** and does not auto-adjust for
> daylight saving. For roughly **7am ET**, use `0 11 * * *` during EDT
> (Mar–Nov) or `0 12 * * *` during EST (Nov–Mar). The workflow ships with
> `0 11 * * *` and can also be triggered manually from the Actions tab.

## Configuration

Set these as GitHub repo secrets (**Settings → Secrets and variables →
Actions**), or as environment variables / `.env` for local runs:

| Variable | Required | Default | Notes |
| --- | --- | --- | --- |
| `ANTHROPIC_API_KEY` | yes | — | Anthropic API key |
| `EMAIL_SENDER` | for email | — | Sending address |
| `EMAIL_APP_PASSWORD` | for email | — | App password, **not** your account password |
| `EMAIL_RECIPIENT` | for email | — | Recipient (or comma-separated list) |
| `SMTP_HOST` | no | `smtp.gmail.com` | |
| `SMTP_PORT` | no | `465` | SSL port |

> **Gmail note:** `EMAIL_APP_PASSWORD` requires 2-factor auth turned on for the
> sending account, then an app password generated at
> [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
> Regular account passwords will not work with SMTP.

## Running locally

```bash
pip install -r requirements.txt

# Streamlit app
streamlit run streamlit_app.py

# Build the digest and send it once
python scripts/run_digest_and_email.py
```
