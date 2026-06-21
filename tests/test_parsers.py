"""Unit tests for the pure parsing / formatting helpers.

These functions turn Claude's markdown output into the structured pieces the UI
and the email render. They're regex-driven and the most fragile part of the app,
so they're worth pinning down. Nothing here calls the Claude API — the tests run
against fixed sample briefs.
"""

import shared
from shared import md_to_html
from views.daily_update import parse_digest_sections
from views.search import (
    parse_related_topics,
    parse_section,
    parse_sentiment_score,
    parse_signals,
    strip_sentiment_score,
)

# A representative digest in the exact format run_daily_digest() asks Claude for.
DIGEST_SAMPLE = """**MARKETING & ADVERTISING**

• Story one. [Ad Age](https://adage.com)

**DIGITAL MARKETING**

• Story two. [MarTech](https://martech.org)

**CROSS-SOURCE THEMES**

• A shared theme. [Digiday](https://digiday.com)
"""

# A representative trend brief in the format run_research() asks for.
SEARCH_SAMPLE = """**TOP STORY**

The big thing happened. [TechCrunch](https://techcrunch.com)

**NARRATIVE THREADS**

• **Thread one**: details here. [Source](https://example.com)

**SENTIMENT SNAPSHOT**

Mood is broadly positive. **growth**
Score: Optimistic

**EMERGING SIGNAL**

Watch this early signal. [Source](https://example.com)

**SO WHAT**

Do the thing now.

**LEARN MORE**

• [Guide](https://example.com) — covers the basics.

**TREND SIGNALS**

AI agents, vibe marketing, retail media, social commerce

**RELATED TOPICS**

programmatic ads, influencer roi, brand safety
"""


# --- md_to_html -----------------------------------------------------------

def test_md_to_html_renders_link():
    out = md_to_html("See [Ad Age](https://adage.com)")
    assert '<a href="https://adage.com" target="_blank" rel="noopener noreferrer">Ad Age</a>' in out


def test_md_to_html_renders_bold():
    assert md_to_html("**big news**") == "<strong>big news</strong>"


def test_md_to_html_collapses_newlines_to_br():
    assert md_to_html("a\n\nb") == "a<br>b"


def test_md_to_html_escapes_raw_html():
    out = md_to_html("<script>alert(1)</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_md_to_html_escapes_ampersand_in_text():
    # Common in marketing copy ("M&A", "P&G") — must become a valid entity.
    assert md_to_html("M&A activity") == "M&amp;A activity"


def test_md_to_html_keeps_link_with_query_string():
    out = md_to_html("[x](https://x.com?a=1&b=2)")
    # The ampersand is escaped inside the href (valid HTML) and the tag still forms.
    assert '<a href="https://x.com?a=1&amp;b=2"' in out
    assert ">x</a>" in out


# --- parse_digest_sections ------------------------------------------------

def test_parse_digest_sections_splits_by_header():
    headers = [h for h, _ in parse_digest_sections(DIGEST_SAMPLE)]
    assert headers == [
        "MARKETING & ADVERTISING",
        "DIGITAL MARKETING",
        "CROSS-SOURCE THEMES",
    ]


def test_parse_digest_sections_attaches_body():
    sections = dict(parse_digest_sections(DIGEST_SAMPLE))
    assert "Story one" in sections["MARKETING & ADVERTISING"]
    assert "Story two" in sections["DIGITAL MARKETING"]


def test_parse_digest_sections_no_headers_returns_empty():
    assert parse_digest_sections("plain text with no section headers") == []


# --- parse_section --------------------------------------------------------

def test_parse_section_extracts_body():
    assert "The big thing happened" in parse_section(SEARCH_SAMPLE, "TOP STORY")


def test_parse_section_stops_at_next_header():
    top = parse_section(SEARCH_SAMPLE, "TOP STORY")
    assert "NARRATIVE THREADS" not in top
    assert "Thread one" not in top


def test_parse_section_missing_returns_empty():
    assert parse_section(SEARCH_SAMPLE, "NONEXISTENT SECTION") == ""


# --- parse_signals / parse_related_topics ---------------------------------

def test_parse_signals_splits_and_limits():
    signals = parse_signals(SEARCH_SAMPLE)
    assert "AI agents" in signals
    assert "social commerce" in signals
    assert len(signals) == 4


def test_parse_signals_caps_at_six():
    many = "**TREND SIGNALS**\n\na one, b two, c three, d four, e five, f six, g seven, h eight"
    assert len(parse_signals(many)) == 6


def test_parse_related_topics():
    topics = parse_related_topics(SEARCH_SAMPLE)
    assert "programmatic ads" in topics
    assert len(topics) == 3


# --- sentiment score ------------------------------------------------------

def test_parse_sentiment_score():
    snap = parse_section(SEARCH_SAMPLE, "SENTIMENT SNAPSHOT")
    assert parse_sentiment_score(snap) == "Optimistic"


def test_parse_sentiment_score_missing_returns_empty():
    assert parse_sentiment_score("no score mentioned here") == ""


def test_strip_sentiment_score_removes_score_line():
    snap = parse_section(SEARCH_SAMPLE, "SENTIMENT SNAPSHOT")
    stripped = strip_sentiment_score(snap)
    assert "Score:" not in stripped
    assert "Mood is broadly positive" in stripped


# --- shared generation constants (regression guard for the centralized values)

def test_generation_constants_unchanged():
    assert shared.MAX_TOKENS == 4096
    assert shared.MAX_AGENT_ROUNDS == 5
