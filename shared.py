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

# Cost controls on web search (the dominant cost of a run):
#   • web_search_20260209 adds *dynamic filtering* — Claude filters results before
#     they enter the context window, cutting the input-token cost. Supported on
#     Sonnet 4.6 and Opus 4.6/4.7/4.8; the under-the-hood code execution is free
#     alongside web search, and no separate code_execution tool is declared.
#   • max_uses caps how many searches a single run may make, bounding both the
#     per-search charge and the result tokens pulled into context.
# Fallback: if the account doesn't have code execution enabled, set the type back
# to "web_search_20250305" (basic search, no dynamic filtering).
SEARCH_TOOL = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}]


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
