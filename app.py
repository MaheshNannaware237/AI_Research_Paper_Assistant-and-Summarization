"""
AI Research Paper Assistant
Powered by Groq (Free) + Streamlit Cloud
"""

import streamlit as st
import os
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from dotenv import load_dotenv

load_dotenv()

def create_summary_pdf(summary_text):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Research Paper Summary", styles["Title"]),
        Paragraph(summary_text.replace("\n", "<br/>"), styles["BodyText"])
    ]

    doc.build(content)

    buffer.seek(0)
    return buffer

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:       #0d0f14;
    --surface:  #141820;
    --surface2: #1c2230;
    --border:   #252d3d;
    --accent:   #4f8ef7;
    --accent2:  #7c5cfc;
    --gold:     #f0c040;
    --text:     #e8eaf0;
    --muted:    #8892aa;
    --success:  #34d399;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem; max-width: 1300px; }

.hero {
    background: linear-gradient(135deg, #141820 0%, #1a1f2e 50%, #141820 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(79,142,247,0.12) 0%, transparent 70%);
}
.hero::after {
    content: '';
    position: absolute; bottom: -80px; left: -40px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(124,92,252,0.10) 0%, transparent 70%);
}
.hero-badge {
    display: inline-block;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.3);
    color: var(--accent);
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 0.25rem 0.75rem; border-radius: 20px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem; font-weight: 700;
    background: linear-gradient(135deg, #e8eaf0 30%, #4f8ef7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2; margin: 0 0 0.5rem;
}
.hero-sub { color: var(--muted); font-size: 1.05rem; font-weight: 300; }

.stat-row { display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 130px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.25rem; text-align: center;
}
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem; font-weight: 500;
    color: var(--accent); line-height: 1;
}
.stat-label { font-size: 0.78rem; color: var(--muted); margin-top: 0.3rem; letter-spacing: 0.05em; text-transform: uppercase; }

.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
}
.section-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem; margin: 0 0 0.75rem;
    color: var(--gold);
}

.qa-question {
    background: rgba(79,142,247,0.08);
    border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.2rem;
    margin: 0.75rem 0 0.4rem; font-weight: 500;
}
.qa-answer {
    background: var(--surface2);
    border-left: 3px solid var(--success);
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.2rem; margin-bottom: 0.75rem;
    line-height: 1.7;
}
.qa-source {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.9rem; margin: 0.3rem 0;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface); border-radius: 10px;
    padding: 4px; gap: 4px; border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; color: var(--muted);
    font-weight: 500; padding: 0.5rem 1.25rem; font-size: 0.88rem;
}
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: #fff !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: white; border: none; border-radius: 10px;
    padding: 0.55rem 1.6rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600; font-size: 0.9rem;
    transition: opacity 0.2s, transform 0.15s;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

.stTextArea textarea, .stTextInput input {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 6px; }
hr { border-color: var(--border) !important; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
from utils.pdf_reader import extract_text_from_pdf, get_pdf_metadata
from utils.text_splitter import split_text, split_by_sections
from utils.groq_api import generate_summary, generate_section_summaries, answer_question

# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "extracted_text": "",
        "chunks": [],
        "summary": "",
        "section_summaries": {},
        "qa_history": [],
        "pdf_meta": {},
        "file_name": "",
        "ready": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── Check API key (from .env locally or Streamlit secrets on cloud) ───────────
def get_api_key():
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass
    return key

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:0.5rem 0 1.5rem;'>
        <div style='font-size:2.5rem;'>🔬</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.1rem; color:#e8eaf0; font-weight:700;'>Research Assistant</div>
        <div style='font-size:0.75rem; color:#8892aa; margin-top:0.2rem;'>Powered by Groq · Free · Fast</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📄 Upload Paper")
    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}**")
        st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    chunk_size = st.slider("Chunk size (chars)", 1000, 5000, 3000, 500)
    top_k = st.slider("Context chunks for Q&A", 2, 8, 4)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.8rem; color:#8892aa; line-height:2;'>
    🤖 <b style='color:#e8eaf0;'>Model</b><br>
    &nbsp;&nbsp;Llama 3 (8B) via Groq<br><br>
    💾 <b style='color:#e8eaf0;'>RAM Usage</b><br>
    &nbsp;&nbsp;~150 MB only<br><br>
    ⚡ <b style='color:#e8eaf0;'>Speed</b><br>
    &nbsp;&nbsp;5–15 seconds<br><br>
    💰 <b style='color:#e8eaf0;'>Cost</b><br>
    &nbsp;&nbsp;100% Free
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.ready:
        st.markdown("---")
        if st.button("🗑️ Clear & Reset", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔬 Groq · Llama 3 · Free · Streamlit Cloud</div>
    <div class="hero-title">AI Research Paper Assistant</div>
    <div class="hero-sub">
        Upload any academic PDF — get instant AI summaries, section breakdowns,
        and ask questions answered directly from the paper. 100% Free.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Gate: no PDF ──────────────────────────────────────────────────────────────
if uploaded_file is None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="section-card" style="text-align:center;">
            <div style="font-size:2rem;">📑</div>
            <h3 style="color:#4f8ef7;">Smart Summarisation</h3>
            <p style="color:#8892aa; font-size:0.88rem;">Llama 3 condenses long papers into clear structured summaries instantly.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="section-card" style="text-align:center;">
            <div style="font-size:2rem;">💬</div>
            <h3 style="color:#7c5cfc;">Q&A over Paper</h3>
            <p style="color:#8892aa; font-size:0.88rem;">Ask anything — AI finds and answers from the paper's content directly.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="section-card" style="text-align:center;">
            <div style="font-size:2rem;">🗂️</div>
            <h3 style="color:#f0c040;">Section Analysis</h3>
            <p style="color:#8892aa; font-size:0.88rem;">Auto-detects and summarises Abstract, Methods, Results, and more.</p>
        </div>""", unsafe_allow_html=True)
    st.info("👈 Upload a research paper PDF using the sidebar to get started.")
    st.stop()

# ── Process PDF ───────────────────────────────────────────────────────────────
if uploaded_file.name != st.session_state.file_name:
    st.session_state.file_name = uploaded_file.name
    st.session_state.ready = False
    st.session_state.summary = ""
    st.session_state.section_summaries = {}
    st.session_state.qa_history = []

    with st.status("🔄 Processing your paper…", expanded=True) as status:
        st.write("📖 Extracting text from PDF…")
        pdf_bytes = uploaded_file.read()
        st.session_state.extracted_text = extract_text_from_pdf(io.BytesIO(pdf_bytes))
        st.session_state.pdf_meta = get_pdf_metadata(io.BytesIO(pdf_bytes))

        st.write("✂️ Splitting into chunks…")
        st.session_state.chunks = split_text(
            st.session_state.extracted_text,
            chunk_size=chunk_size,
        )

        st.session_state.ready = True
        status.update(label="✅ Paper ready! No models loaded — instant start.", state="complete")

# ── Stats ─────────────────────────────────────────────────────────────────────
meta = st.session_state.pdf_meta
word_count = len(st.session_state.extracted_text.split())
char_count = len(st.session_state.extracted_text)

st.markdown(f"""
<div class="stat-row">
    <div class="stat-card"><div class="stat-value">{meta.get('pages','—')}</div><div class="stat-label">Pages</div></div>
    <div class="stat-card"><div class="stat-value">{word_count:,}</div><div class="stat-label">Words</div></div>
    <div class="stat-card"><div class="stat-value">{len(st.session_state.chunks)}</div><div class="stat-label">Chunks</div></div>
    <div class="stat-card"><div class="stat-value">{char_count:,}</div><div class="stat-label">Characters</div></div>
</div>
""", unsafe_allow_html=True)

if meta.get("title") and meta["title"] != "Unknown":
    st.caption(f"📌 **Title:** {meta['title']}   |   **Author:** {meta.get('author','Unknown')}")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Extracted Text",
    "📑 Summary",
    "🗂️ Section Analysis",
    "💬 Ask Questions",
])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("#### Raw Extracted Text")
    preview = st.slider("Preview length (chars)", 1000, min(20000, char_count), 5000, 500)
    st.text_area("", st.session_state.extracted_text[:preview], height=420, label_visibility="collapsed")
    if char_count > preview:
        st.caption(f"Showing {preview:,} of {char_count:,} characters.")
    with st.expander("📋 PDF Metadata"):
        for k, v in meta.items():
            st.markdown(f"**{k.title()}:** `{v}`")

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("#### AI-Generated Summary")
    st.caption("Llama 3 reads the full paper and returns a structured summary in seconds.")

    if st.session_state.summary:
       st.markdown(f"""
        <div class="section-card">
        <p style="line-height:1.9; font-size:0.95rem; white-space:pre-wrap;">{st.session_state.summary}</p>
        </div>""", unsafe_allow_html=True)

    pdf_file = create_summary_pdf(st.session_state.summary)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "📄 Download PDF",
            data=pdf_file,
            file_name="research_paper_summary.pdf",
            mime="application/pdf"
        )

    with col2:
        st.download_button(
            "📝 Download TXT",
            data=st.session_state.summary,
            file_name="research_paper_summary.txt",
            mime="text/plain"
        )

    with col3:
        if st.button("🔄 Regenerate"):
            st.session_state.summary = ""
            st.rerun()
        else:
          if st.button("🚀 Generate Summary"):
            with st.spinner("Llama 3 is reading the paper… (~5–15 sec)"):
                try:
                    st.session_state.summary = generate_summary(st.session_state.extracted_text)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
          else:
            st.info("Click **Generate Summary** to analyse the paper.")

# ── TAB 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("#### Section-by-Section Analysis")
    st.caption("Auto-detects paper sections and summarises each with Llama 3.")

    sections = split_by_sections(st.session_state.extracted_text)

    if not sections:
        st.warning("Could not auto-detect sections. The paper may use non-standard headings.")
    else:
        st.success(f"Found **{len(sections)}** section(s): {', '.join(sections.keys())}")

        if st.session_state.section_summaries:
            for name, summ in st.session_state.section_summaries.items():
                st.markdown(f"""
                <div class="section-card">
                    <h3>{name}</h3>
                    <p style="line-height:1.8; font-size:0.9rem; color:#c8ccd8;">{summ}</p>
                </div>""", unsafe_allow_html=True)
        else:
            if st.button("🗂️ Summarise All Sections"):
                with st.spinner("Summarising each section…"):
                    try:
                        st.session_state.section_summaries = generate_section_summaries(sections)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                for name, content in sections.items():
                    with st.expander(f"📌 {name}"):
                        st.text(content[:1500] + ("…" if len(content) > 1500 else ""))

# ── TAB 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("#### Ask Questions About This Paper")
    st.caption("Type any question — Llama 3 answers using only the paper's content.")

    question = st.text_input(
        "", placeholder="e.g. What dataset was used? What is the main contribution?",
        label_visibility="collapsed",
    )

    col_ask, col_clear = st.columns([1, 5])
    with col_ask:
        ask_btn = st.button("💬 Ask", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear History"):
            st.session_state.qa_history = []
            st.rerun()

    if ask_btn and question.strip():
        with st.spinner("Searching the paper…"):
            try:
                ans, sources = answer_question(question, st.session_state.chunks, top_k=top_k)
                st.session_state.qa_history.append({"q": question, "a": ans, "sources": sources})
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

    if st.session_state.qa_history:
        st.markdown("---")
        for i, item in enumerate(reversed(st.session_state.qa_history)):
            st.markdown(f"""
            <div class="qa-question">❓ {item['q']}</div>
            <div class="qa-answer">💡 {item['a']}</div>
            """, unsafe_allow_html=True)
            with st.expander(f"📚 Source passages used"):
                for j, src in enumerate(item["sources"], 1):
                    st.markdown(f"<div class='qa-source'><b>Chunk {j}:</b> {src[:400]}{'…' if len(src)>400 else ''}</div>", unsafe_allow_html=True)
    else:
        st.info("Ask a question above and the answer will appear here.")
