"""Daily Update page — preview the marketing/branding digest on demand.

Generation is button-triggered (not on page load) so the app only spends when
someone explicitly asks for it; the scheduled morning email is the one
guaranteed daily run.
"""

import re
from datetime import datetime

import streamlit as st

from digest import DIGEST_SOURCES, run_daily_digest
from shared import md_to_html

DIGEST_CARD_CLASSES = ["card-green", "card-blue", "card-purple", "card-amber"]


def parse_digest_sections(text: str) -> list[tuple[str, str]]:
    """Split the digest into (header, body) pairs by its **ALL CAPS** headers."""
    matches = list(re.finditer(r'^\*\*([A-Z][A-Z0-9 &/\-]{2,})\*\*\s*$', text, re.MULTILINE))
    sections = []
    for idx, m in enumerate(matches):
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((m.group(1).strip(), body))
    return sections


def _display_digest(raw: str, fetched_at: str) -> None:
    st.divider()
    c1, c2 = st.columns([3, 1])
    with c1:
        st.caption(f"🕐 Generated {fetched_at}")
    with c2:
        st.download_button(
            "⬇ Export",
            data=raw,
            file_name="daily-digest.md",
            mime="text/markdown",
            use_container_width=True,
        )

    sections = parse_digest_sections(raw)
    if not sections:
        st.markdown(raw)
        return

    for i, (header, body) in enumerate(sections):
        cls = "card-slate" if "CROSS" in header else DIGEST_CARD_CLASSES[i % len(DIGEST_CARD_CLASSES)]
        st.markdown(f'<p class="meta-label">{header.title()}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="{cls}">{md_to_html(body)}</div>', unsafe_allow_html=True)

    with st.expander("📄 Raw output"):
        st.markdown(raw)


def render() -> None:
    st.title("📰 Daily Update")
    st.caption(
        "Marketing, branding, digital & social media news from the last 24–48h — "
        "the same brief that's emailed each morning."
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        clicked = st.button("▶  Generate / Refresh", type="primary", use_container_width=True)

    with st.expander("Sources covered"):
        for category, pubs in DIGEST_SOURCES.items():
            st.markdown(f"**{category}** — {', '.join(pubs)}")

    if clicked:
        try:
            with st.status("Compiling the daily digest…", expanded=True) as status:
                digest_raw = run_daily_digest(on_step=st.write)
                status.update(label="Digest ready", state="complete", expanded=False)
            st.session_state.update(
                digest_raw=digest_raw,
                digest_fetched_at=datetime.now().strftime("%d %b %Y, %H:%M"),
            )
        except RuntimeError as exc:
            st.error(str(exc))

    raw = st.session_state.get("digest_raw")
    if not raw:
        st.info(
            "Click **Generate / Refresh** to compile today's digest. "
            "It runs a handful of web searches and takes ~15–30s."
        )
        return

    _display_digest(raw, st.session_state.get("digest_fetched_at", ""))
