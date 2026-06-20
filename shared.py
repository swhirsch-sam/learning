"""Shared helpers used by both the Streamlit app and the headless digest.

Keeping the client, model config, and markdown→HTML helper here (rather than in
``streamlit_app.py``) lets ``digest.py`` and the CI script reuse them without
importing Streamlit or executing the whole page at import time.
"""

import os
import re

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"

# Web search cost control: max_uses caps how many searches a single run may make,
# bounding both the per-search charge ($10 / 1,000 searches) and the result tokens
# pulled into context.
#
# Using the basic search tool (web_search_20250305) by default — it has no extra
# account requirements. To further cut the input-token cost, upgrade the type to
# "web_search_20260209" for *dynamic filtering* (Claude filters results before they
# enter the context window). That variant runs code execution under the hood, so
# the account must have code execution enabled in the Claude Console.
SEARCH_TOOL = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 8}]


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client, raising if the API key is missing.

    The Streamlit app wraps this with caching and a friendlier error; headless
    callers (the digest script) just let the exception propagate.
    """
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set.")
    return anthropic.Anthropic(api_key=key)


def md_to_html(text: str) -> str:
    """Convert the lightweight markdown Claude emits (links, bold, line breaks)
    into the inline HTML used by both the app cards and the digest email."""
    text = re.sub(
        r'\[([^\]]+)\]\((https?://[^\)]+)\)',
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        text,
    )
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\n+', '<br>', text)
    return text
