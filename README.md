# Trend Intelligence Dashboard

A Streamlit app that turns any topic into a structured trend brief — researched live from the web and synthesized by Claude.

Type in a topic (e.g. "generative AI", "climate tech", "fintech") and the app uses [Claude](https://www.anthropic.com/claude)'s web search tool to gather current sources, then organizes the findings into a scannable brief:

- **Top story** — the single most significant recent development, with a citation
- **Narrative threads** — the 2–3 storylines driving the conversation
- **Sentiment snapshot** — an overall mood read (Optimistic / Mixed / Cautious / Uncertain), color-coded
- **Emerging signal** — one early-stage development worth watching
- **So what** — the practical takeaway
- **Learn more** — a short reading list with live links
- **Trend signals** and **related topics** — clickable chips for jumping to adjacent searches

Briefs can be exported as Markdown, and a **Raw Output** tab shows the unprocessed model response for anyone who wants to see exactly what Claude returned.

## Running locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Provide an Anthropic API key, either as an environment variable or in a `.env` file:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Launch the app:
   ```bash
   streamlit run app.py
   ```

## Stack

- [Streamlit](https://streamlit.io/) for the interface
- [Claude](https://www.anthropic.com/claude) (`claude-sonnet-4-6`) with the web search tool for live research and synthesis, via the [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)

`streamlit_app.py` is a duplicate of `app.py`, kept in sync for compatibility with Streamlit Community Cloud's default entry-point naming.
