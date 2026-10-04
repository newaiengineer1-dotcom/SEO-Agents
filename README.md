# SEO Premium Agent — CrewAI + Groq + Streamlit

A modular Streamlit application that audits a website and runs six specialist SEO agents:

1. Technical SEO Architect
2. Keyword & Content Strategist
3. On-Page SEO Copywriter
4. UX & Premium Web Designer
5. Authority & Growth Strategist
6. SEO QA & Release Reviewer

## Important architecture choice
This project intentionally avoids the fragile `groq/...` LiteLLM route. CrewAI is configured with `custom_openai=True` and Groq's OpenAI-compatible endpoint:
`https://api.groq.com/openai/v1`.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Paste the Groq key in the sidebar at runtime. Do not commit the key to GitHub.

## What it does
- Fetches the target URL and collects evidence: status, title, description, canonical, headings, text size, image alt coverage, internal/external links, viewport, robots.txt, sitemap.xml and JSON-LD schema.
- Shows an evidence dashboard before AI recommendations.
- Sends the evidence and supplied business context/keywords to six specialist CrewAI agents.
- Produces implementation-ready technical SEO, keyword, copy, UX/UI, growth and QA recommendations.
- Generates a downloadable Markdown report.

## What it does NOT claim
No AI tool can guarantee a Google/Bing ranking position. Recommendations must be validated in staging, implemented on the real site/CMS, and measured in analytics/search-console tooling.

## Testing
```bash
python -m compileall .
pytest -q
```

## GitHub UI upload
1. Create a new GitHub repository.
2. Upload the complete project folder contents.
3. Commit to `main`.
4. Do not upload `.env`, API keys, credentials, or private client data.

## Streamlit Community Cloud
1. Sign in at Streamlit Community Cloud with GitHub.
2. Connect GitHub.
3. Create app → choose the repository → branch `main` → entrypoint `app.py`.
4. Deploy.
5. Open app Settings → Secrets and add a secret only if you later change the app to read from `st.secrets`. The current version intentionally accepts the key in the session sidebar.

For current deployment requirements, see Streamlit's documentation.
