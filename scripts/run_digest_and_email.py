"""Headless entry point: build the daily digest and email it.

Run from CI (or locally) with ``python scripts/run_digest_and_email.py``.
Requires ANTHROPIC_API_KEY plus the EMAIL_* variables (see mailer.py / README).
"""

import os
import sys
from datetime import datetime

# Allow `python scripts/run_digest_and_email.py` from the repo root by putting
# the project root (this file's parent's parent) on the import path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from digest import run_daily_digest
from mailer import send_email
from shared import md_to_html


def main() -> None:
    digest_md = run_daily_digest()
    html = md_to_html(digest_md)
    subject = f"Daily Marketing Digest — {datetime.now():%b %d, %Y}"
    send_email(subject=subject, html_body=html)
    print(f"Sent: {subject}")


if __name__ == "__main__":
    main()
