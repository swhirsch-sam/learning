# Intelligence Hub

A Streamlit app that uses Claude + web search to produce real-time intelligence —
on-demand trend briefs and an automated daily marketing digest. Deployed at
[pulseagent.streamlit.app](https://pulseagent.streamlit.app).

Everything runs on Claude's built-in `web_search` tool (Claude searches the web
directly and returns a structured markdown brief). There are no scrapers, RSS
parsers, or third-party automation/email services.

## Features

The app is two tools, each its own page (native sidebar navigation). **Daily
Update** is the default landing page; **Search** is the second.

### 📰 Daily Update
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

In the app, the digest is generated **on demand** via the **Generate / Refresh**
button (it isn't auto-run on page load, so you only spend when you ask). The
scheduled morning email is the one guaranteed daily run.

### 🔍 Search
Enter any topic and get a structured brief — top story, narrative threads, a
sentiment snapshot, an emerging signal, "so what", and resources — synthesized
from live web search.

### Web search & cost

Both tools use Claude's `web_search` tool with two cost controls (in
`shared.py`): the **dynamic-filtering** version (`web_search_20260209`), which
filters results before they enter the context window, and a **`max_uses`** cap
that bounds searches per run. A typical digest run costs roughly **$0.20–$0.40**
on Sonnet 4.6 ($10 / 1,000 searches + token costs).

> Dynamic filtering runs server-side code execution under the hood — your
> account must have **web search and code execution enabled** in the Claude
> Console. If code execution isn't available, set the tool `type` in `shared.py`
> back to `web_search_20250305` (basic search, no filtering).

## Layout

| File | Purpose |
| --- | --- |
| `streamlit_app.py` | Entry point / router: page config, shared CSS, `st.navigation`. `app.py` is a deploy-time mirror. |
| `views/daily_update.py` | Daily Update page (digest preview) |
| `views/search.py` | Search page (`run_research()` + trend-brief UI) |
| `digest.py` | `DIGEST_SOURCES` and `run_daily_digest()` |
| `mailer.py` | `send_email()` — stdlib `smtplib` over SSL |
| `shared.py` | Shared client/model config, web-search tool, markdown→HTML helper |
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
