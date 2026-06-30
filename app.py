from dotenv import load_dotenv
load_dotenv()

import base64
import io
import os

import pdf2image
import streamlit as st
from google import genai
from google.genai import types

# ── Gemini config ─────────────────────────────────────────────────────────────
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body { font-family: 'Inter', sans-serif !important; }

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 55%, #24243e 100%);
}
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* Global text */
p, li, span { color: #cbd5e1; }
h1, h2, h3  { color: #f1f5f9 !important; }

/* Text area */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(129,140,248,0.6) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.12) !important;
}
label { color: #94a3b8 !important; font-size: 13px !important; }

/* File uploader */
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.04);
    border: 2px dashed rgba(129,140,248,0.35);
    border-radius: 12px;
    padding: 10px;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"] section:hover {
    border-color: rgba(167,139,250,0.65);
}
[data-testid="stFileUploader"] section p { color: #94a3b8 !important; }

/* Primary buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.02em !important;
    padding: 0.6rem 1rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Download button override */
[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: #a78bfa !important;
    font-size: 13px !important;
    padding: 0.4rem 1rem !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(167,139,250,0.15) !important;
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #818cf8 !important; }

/* Divider */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 1rem 0 !important; }

/* Alerts */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* Markdown output from AI (result card) */
.result-card .stMarkdown p,
.result-card .stMarkdown li { color: #e2e8f0 !important; line-height: 1.8; font-size: 14.5px; }
.result-card .stMarkdown h2,
.result-card .stMarkdown h3 { color: #a78bfa !important; }
.result-card .stMarkdown strong { color: #f1f5f9 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(129,140,248,0.35); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Prompts ───────────────────────────────────────────────────────────────────

PROMPT_REVIEW = """
You are an experienced Technical Human Resource Manager.
Review the provided resume against the job description and give a structured evaluation:

**Overall Alignment:** (Poor / Fair / Good / Excellent)

**Key Strengths:**
- Highlight the top 3–5 skills/experiences that match the role

**Gaps & Weaknesses:**
- List important requirements the candidate is missing

**Standout Qualities:**
- Note anything impressive or unique about the candidate

**Verdict:**
A concise 2–3 sentence hiring recommendation.
"""

PROMPT_ATS = """
You are a skilled ATS (Applicant Tracking System) scanner with deep knowledge of
recruitment software and keyword matching.

Evaluate the resume against the job description and respond in exactly this format:

**Match Score:** X%

**Missing Keywords:**
- List every important keyword, skill, or certification absent from the resume

**Keywords Found:**
- List the matching skills, tools, and keywords present

**Final Thoughts:**
2–3 sentences summarising whether the candidate should apply and what to fix first.
"""

PROMPT_IMPROVE = """
You are a professional resume coach and career strategist.
Analyse the resume against the job description and give specific, actionable advice:

**Quick Wins** *(add these immediately)*:
- ...

**Skills to Develop:**
- ...

**Tailoring Tips** *(how to customise for this exact role)*:
- ...

**Formatting & Structure Advice:**
- ...

Keep every suggestion concrete and specific to this resume and job description.
"""


# ── Helper functions ──────────────────────────────────────────────────────────

def pdf_to_image_part(file_bytes: bytes):
    images = pdf2image.convert_from_bytes(file_bytes,
                poppler_path=r"C:\Program Files (x86)\poppler\Library\bin"   # ← change this to your actual path
    )
    
    buf = io.BytesIO()
    images[0].save(buf, format="JPEG")
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def call_gemini(system_prompt: str, image_part, job_desc: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",   # ← changed from gemini-2.0-flash
        contents=[system_prompt, image_part, job_desc]
    )
    return response.text
def run_analysis(prompt: str, label: str, icon: str) -> None:
    """Validate inputs, run Gemini, and render the result."""
    job_text = st.session_state.get("job_text", "").strip()
    resume_bytes = st.session_state.get("resume_bytes")

    if not job_text:
        st.warning("⚠️ Please paste a job description before running analysis.")
        return
    if not resume_bytes:
        st.warning("⚠️ Please upload your resume (PDF) before running analysis.")
        return

    with st.spinner("🤖 Gemini is analysing your resume…"):
        try:
            image_part = pdf_to_image_part(resume_bytes)
            result = call_gemini(prompt, image_part, job_text)
        except Exception as exc:
            st.error(f"❌ Something went wrong: {exc}")
            return

    # Section label
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;margin:1.5rem 0 0.5rem;">
        <span style="font-size:1.4rem;">{icon}</span>
        <span style="color:#a78bfa;font-size:0.8rem;font-weight:700;
                     text-transform:uppercase;letter-spacing:0.12em;">{label}</span>
    </div>
    """, unsafe_allow_html=True)

    # Result card wrapper (CSS class targets markdown children)
    st.markdown("""
    <div class="result-card" style="background:rgba(99,102,241,0.07);
         border:1px solid rgba(99,102,241,0.22);border-radius:14px;
         padding:20px 24px;margin-bottom:1rem;">
    """, unsafe_allow_html=True)
    st.markdown(result)          # renders AI markdown correctly
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download analysis",
        data=result,
        file_name=f"ats_{label.lower().replace(' ', '_')}.txt",
        mime="text/plain",
    )


# ── UI ────────────────────────────────────────────────────────────────────────

def section_label(text: str, top_margin: str = "0") -> None:
    st.markdown(
        f'<p style="color:#a78bfa;font-size:0.78rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:0.12em;'
        f'margin:{top_margin} 0 6px;">{text}</p>',
        unsafe_allow_html=True,
    )


# Header
st.markdown("""
<div style="text-align:center;padding:0.25rem 0 1.75rem;">
    <div style="font-size:2.8rem;line-height:1;margin-bottom:0.6rem;">🎯</div>
    <h1 style="margin:0;font-size:2.3rem;font-weight:800;
               background:linear-gradient(135deg,#818cf8,#a78bfa,#c084fc);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;">
        ATS Resume Expert
    </h1>
    <p style="color:#475569;font-size:0.95rem;margin-top:0.4rem;font-weight:400;">
        Powered by Google Gemini 2.5 Flash · AI-driven resume intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input row ──
col_jd, col_cv = st.columns(2, gap="large")

with col_jd:
    section_label("📋 Job Description")
    job_input = st.text_area(
        "jd",
        height=240,
        placeholder="Paste the full job description here…",
        label_visibility="collapsed",
    )
    st.session_state.job_text = job_input

with col_cv:
    section_label("📄 Your Resume (PDF)")
    uploaded = st.file_uploader("resume", type=["pdf"], label_visibility="collapsed")

    if uploaded is not None:
        # Store raw bytes so reruns can re-read without cursor issues
        st.session_state.resume_bytes = uploaded.getvalue()
        st.session_state.resume_name = uploaded.name

    if st.session_state.get("resume_bytes"):
        size_kb = len(st.session_state.resume_bytes) / 1024
        name = st.session_state.get("resume_name", "resume.pdf")
        st.markdown(f"""
        <div style="margin-top:10px;display:flex;align-items:center;gap:10px;
                    background:rgba(34,197,94,0.09);
                    border:1px solid rgba(34,197,94,0.28);
                    border-radius:10px;padding:10px 14px;">
            <span style="font-size:1.3rem;">✅</span>
            <div>
                <div style="color:#4ade80;font-weight:600;font-size:13px;margin-bottom:2px;">{name}</div>
                <div style="color:#475569;font-size:11.5px;">{size_kb:.1f} KB · Ready for analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Action buttons ──
section_label("⚡ Choose Analysis", top_margin="1.4rem")

ANALYSES = [
    ("🔍", "Resume Review",   "HR-style strengths & gaps",  PROMPT_REVIEW),
    ("📊", "ATS Score",       "Match % + missing keywords",  PROMPT_ATS),
    ("💡", "Improve Resume",  "Tailored tips to boost score", PROMPT_IMPROVE),
]

btn_cols = st.columns(3, gap="medium")
clicks = {}
for col, (icon, title, tooltip, _) in zip(btn_cols, ANALYSES):
    with col:
        # Info card above button
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);
                    border-radius:10px;padding:12px 14px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:7px;margin-bottom:4px;">
                <span style="font-size:1.15rem;">{icon}</span>
                <span style="color:#e2e8f0;font-weight:600;font-size:13.5px;">{title}</span>
            </div>
            <p style="color:#475569;font-size:12px;margin:0;padding-left:26px;">{tooltip}</p>
        </div>
        """, unsafe_allow_html=True)
        clicks[title] = st.button(f"{icon} Run {title}", key=title, use_container_width=True)

# ── Results ──
st.divider()

for icon, title, _, prompt in ANALYSES:
    if clicks[title]:
        run_analysis(prompt, title, icon)
        break

# ── Footer ──
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 0.25rem;color:#1e293b;font-size:12px;">
    Built with Streamlit &amp; Google Gemini 1.5 Flash
</div>
""", unsafe_allow_html=True)