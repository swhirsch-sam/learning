"""Daily marketing & branding digest.

Mirrors ``run_research()`` in ``streamlit_app.py``: it asks Claude to use the
``web_search`` tool directly and return a structured markdown brief. No
scrapers, RSS libraries, or third-party services — just Claude + web search.

The set of publications is driven entirely by ``DIGEST_SOURCES`` below; the
prompt is built from it dynamically, so swapping a publication in or out is a
one-line edit here with no other code changes.
"""

from shared import MODEL, SEARCH_TOOL, get_client

DIGEST_SOURCES = {
    "Marketing & Advertising": ["Marketing Brew", "Ad Age", "Marketing Dive", "The Drum"],
    "Digital Marketing": ["MarTech", "Search Engine Land", "Digiday"],
    "Branding & Brand Intelligence": ["Branding Strategy Insider", "WARC", "Brandwatch"],
    "Social Media": ["Social Media Today", "Sprout Social Insights"],
}


def _sources_block() -> str:
    """Render DIGEST_SOURCES as a `Category: Pub, Pub, ...` list for the prompt."""
    return "\n".join(
        f"{category}: {', '.join(pubs)}" for category, pubs in DIGEST_SOURCES.items()
    )


def run_daily_digest(on_step=None) -> str:
    client = get_client()

    if on_step:
        on_step("🔍 Scanning marketing & branding publications…")

    other_categories = ", ".join(
        cat.upper() for cat in list(DIGEST_SOURCES)[1:]
    )

    prompt = f"""You are a marketing and branding intelligence analyst. Compile a daily digest of what the publications below have covered in roughly the last 24–48 hours, across marketing, advertising, digital marketing, social media, and branding / brand intelligence.

Sources by category:
{_sources_block()}

Search the web for recent coverage from these named publications. Write one section per category, using the category name in UPPERCASE as the header, in this exact style:

**MARKETING & ADVERTISING**

• One line per relevant story. Cite as [Publication](url). Bold 2–3 key terms.
• Another story…

Repeat one section for each remaining category ({other_categories}), each with 2–4 bullets covering the most relevant recent stories. If a publication has nothing notable in the window, simply skip it — never invent stories or use placeholder links.

After all the per-category sections, add:

**CROSS-SOURCE THEMES**

• 2–4 bullets flagging where multiple sources are converging on the same story or trend. Name the converging sources and bold the shared theme.

Formatting rules:
- Use real, clickable URLs in every bullet: [Publication](https://actual-url.com)
- Bold key terms with **double asterisks** (2–4 word phrases only)
- Keep every bullet to a single tight line — no filler
- Never use # or ## markdown headings — use only the **SECTION NAME** format above"""

    messages = [{"role": "user", "content": prompt}]

    text = ""
    for i in range(5):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            tools=SEARCH_TOOL,
            messages=messages,
        )

        text = "".join(b.text for b in response.content if b.type == "text")

        if response.stop_reason == "end_turn":
            return text

        if response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            if on_step:
                if i == 0:
                    on_step("📊 Reading the latest coverage…")
                elif i == 1:
                    on_step("✍️ Writing the digest…")
        else:
            return text

    return text
