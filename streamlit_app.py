"""Intelligence Hub — entry point / router.

Two tools, each its own page: Daily Update (default landing) and Search.
Page config + shared CSS live here; the actual UIs are in views/.
"""

import streamlit as st

from views import daily_update, search

st.set_page_config(
    page_title="Intelligence Hub",
    page_icon="🔍",
    layout="wide",
)

# Shared card / chip styling, injected once so both pages inherit it.
st.markdown(
    """
<style>
.chip {
    display: inline-block;
    padding: 4px 13px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 500;
    margin: 3px 2px;
    background: #EEF2FF;
    color: #4338CA;
    border: 1px solid #C7D2FE;
}
.meta-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #6B7280;
    margin: 0 0 6px;
}
.card-green   { background:#F0FDF4; border-left:4px solid #16A34A; padding:14px 18px;
                border-radius:0 6px 6px 0; line-height:1.65; margin:6px 0 14px; }
.card-amber   { background:#FFFBEB; border-left:4px solid #D97706; padding:14px 18px;
                border-radius:0 6px 6px 0; line-height:1.65; margin:6px 0; }
.card-purple  { background:#FDF4FF; border-left:4px solid #9333EA; padding:14px 18px;
                border-radius:0 6px 6px 0; line-height:1.65; margin:6px 0; }
.card-slate   { background:#F8FAFC; border-left:4px solid #64748B; padding:14px 18px;
                border-radius:0 6px 6px 0; line-height:1.65; margin:6px 0 14px; }
.card-threads { background:#FAFAFA; border-left:4px solid #D1D5DB; padding:14px 18px;
                border-radius:0 6px 6px 0; line-height:1.75; margin:6px 0 14px; }
.card-blue    { background:#EFF6FF; border-left:4px solid #2563EB; padding:14px 18px;
                border-radius:0 6px 6px 0; line-height:1.65; margin:6px 0; }
.card-green a, .card-amber a, .card-purple a,
.card-slate a, .card-threads a, .card-blue a {
    color: #1D4ED8;
    font-weight: 500;
    text-decoration: underline;
    text-decoration-color: #BFDBFE;
    text-underline-offset: 2px;
}
.card-green a:hover, .card-amber a:hover, .card-purple a:hover,
.card-slate a:hover, .card-threads a:hover, .card-blue a:hover {
    text-decoration-color: #1D4ED8;
}
</style>
""",
    unsafe_allow_html=True,
)

nav = st.navigation(
    [
        st.Page(daily_update.render, title="Daily Update", icon="📰", url_path="daily", default=True),
        st.Page(search.render, title="Search", icon="🔍", url_path="search"),
    ]
)
nav.run()
