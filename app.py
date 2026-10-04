from __future__ import annotations
import streamlit as st
from core.config import DEFAULT_MODEL, SUPPORTED_MODELS
from utils.web_audit import audit_url
from agents.seo_crew import run_seo_crew
from utils.reporting import build_report

st.set_page_config(page_title="SEO Premium Agent", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root{--bg:#07111f;--card:#0d1b2a;--line:#1d344b;--text:#edf6ff;--muted:#9bb0c5;--accent:#55d6be;--accent2:#6ea8fe}
.stApp{background:linear-gradient(145deg,#06101c,#0a1626 55%,#08121e);color:var(--text)}
.block-container{max-width:1450px;padding-top:1.2rem}
.hero{padding:1.2rem 1.4rem;border:1px solid var(--line);border-radius:22px;background:linear-gradient(135deg,#0d1b2a,#10263b);box-shadow:0 18px 55px #0004;margin-bottom:1rem}
.hero h1{margin:0;color:#fff;font-size:2rem}.hero p{color:var(--muted);margin:.35rem 0 0}
.card{padding:1rem;border:1px solid var(--line);border-radius:16px;background:var(--card);height:100%}
.small{color:var(--muted);font-size:.85rem}.ok{color:#67e8f9}.warn{color:#fbbf24}.bad{color:#fb7185}
.stButton>button{border-radius:11px;border:1px solid #2e5d78;background:#12324a;color:#fff;font-weight:700}
/* Premium dark inputs: prevent browser/autofill yellow and keep text white. */
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div, div[data-baseweb="select"] > div{background:#0d1b2a !important;border:1px solid #2a4660 !important;border-radius:10px !important;box-shadow:none !important}
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea{background:#0d1b2a !important;color:#ffffff !important;-webkit-text-fill-color:#ffffff !important;caret-color:#55d6be !important}
div[data-baseweb="input"] input::placeholder, div[data-baseweb="textarea"] textarea::placeholder{color:#91a7bc !important;opacity:1 !important}
div[data-baseweb="input"] input:-webkit-autofill, div[data-baseweb="input"] input:-webkit-autofill:hover, div[data-baseweb="input"] input:-webkit-autofill:focus, div[data-baseweb="textarea"] textarea:-webkit-autofill{-webkit-box-shadow:0 0 0 1000px #0d1b2a inset !important;box-shadow:0 0 0 1000px #0d1b2a inset !important;-webkit-text-fill-color:#ffffff !important}
label, label p{color:#edf6ff !important}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🚀 SEO Premium Agent</h1><p>CrewAI multi-agent SEO audit, premium UX direction, content strategy and release QA — powered by Groq.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ AI Configuration")
    api_key = st.text_input("Groq API Key", type="password", help="Used only for this Streamlit session; do not paste it into GitHub code.")
    model = st.selectbox("Groq model", list(SUPPORTED_MODELS), index=0)
    st.caption("The app uses CrewAI's custom OpenAI-compatible endpoint mode for Groq.")

c1,c2 = st.columns([1.4,1])
with c1:
    url = st.text_input("Website URL", placeholder="https://example.com")
    business = st.text_area("Business / offer context", placeholder="What the company sells, target customer, geography, differentiators...")
with c2:
    keywords = st.text_area("Target keywords", placeholder="primary keyword\nsecondary keyword\nlocation + service")
    st.info("For best recommendations, provide real business facts and target search intent. The agents are instructed not to invent credentials, statistics or claims.")

if "audit" not in st.session_state: st.session_state.audit = None
if "outputs" not in st.session_state: st.session_state.outputs = None

if st.button("🔎 Run Website Audit", type="primary", use_container_width=True):
    if not url.strip(): st.error("Enter a website URL.")
    else:
        try:
            with st.spinner("Auditing technical SEO signals..."):
                st.session_state.audit = audit_url(url)
            st.success("Audit completed.")
        except Exception as e: st.error(f"Audit failed: {e}")

audit = st.session_state.audit
if audit:
    st.subheader("📊 Evidence Dashboard")
    cols = st.columns(6)
    metrics = [("HTTP",audit.status_code),("H1",audit.h1_count),("Words",audit.word_count),("Images",audit.image_count),("Internal Links",audit.internal_links),("Schema",len(audit.schema_types))]
    for col,(label,val) in zip(cols,metrics): col.metric(label,val)
    a,b,c = st.columns(3)
    with a:
        st.markdown('<div class="card"><b>Strengths</b><br>' + ('<br>'.join('• '+x for x in audit.strengths) or '• None detected') + '</div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><b>Issues</b><br>' + ('<br>'.join('• '+x for x in audit.issues) or '• None detected') + '</div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="card"><b>Warnings</b><br>' + ('<br>'.join('• '+x for x in audit.warnings) or '• None detected') + '</div>', unsafe_allow_html=True)

    if st.button("🤖 Run 6-Agent SEO Transformation", type="primary", use_container_width=True):
        if not api_key.strip(): st.error("Enter your Groq API key in the sidebar.")
        else:
            try:
                with st.spinner("Running specialist agents and QA..."):
                    st.session_state.outputs = run_seo_crew(api_key, model, audit.compact_json(), business, keywords)
                st.success("Multi-agent SEO transformation completed.")
            except Exception as e: st.error(f"CrewAI run failed: {e}")

outputs = st.session_state.outputs
if outputs:
    tabs = st.tabs(["Technical SEO","Keywords","Copy","Premium UX/UI","Growth","QA & Release","Final Report"])
    keys = ["technical","keywords","copy","ux","growth","qa"]
    for tab,key in zip(tabs[:6],keys):
        with tab: st.markdown(outputs[key])
    with tabs[6]:
        report = build_report(audit, outputs, business, keywords)
        st.download_button("⬇️ Download Full Markdown Report", report, file_name="premium_seo_report.md", mime="text/markdown", use_container_width=True)
        st.code(report[:12000], language="markdown")
