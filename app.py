"""
MedShield - Healthcare Privacy Protection
A beautiful, local document redaction tool built with Streamlit.
"""

import streamlit as st
import os
import time

# ── Module Imports ───────────────────────────────────────────────
from redactor import redact_text, get_supported_patterns, RedactionResult
from file_processor import (
    process_file,
    create_download_content,
    validate_file,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
)

# ── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="MedShield - Healthcare Privacy Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──────────────────────────────────────────────────
# This is the heart of the visual design — glassmorphism, floating
# cards, gradient accents, smooth animations, premium dark mode.
st.markdown(
    """
<style>
    /* ─── Google Font ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ─── App Background ─────────────────────────────────── */
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #12102e 40%, #1a1033 100%);
        color: #f0eef8;
    }

    /* Hide Streamlit header bar */
    div[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ─── Animated Gradient Title ─────────────────────────── */
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-title {
        background: linear-gradient(90deg, #6C63FF, #4ECDC4, #a78bfa, #6C63FF);
        background-size: 300% auto;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-size: 3.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        animation: gradientShift 4s ease infinite;
        margin-bottom: 0;
        line-height: 1.2;
    }

    /* ─── Pulsing Shield ─────────────────────────────────── */
    @keyframes pulseGlow {
        0%   { transform: scale(1);   filter: drop-shadow(0 0 0px rgba(108,99,255,0)); }
        50%  { transform: scale(1.12); filter: drop-shadow(0 0 18px rgba(78,205,196,0.6)); }
        100% { transform: scale(1);   filter: drop-shadow(0 0 0px rgba(108,99,255,0)); }
    }
    .shield-icon {
        display: inline-block;
        font-size: 4rem;
        animation: pulseGlow 2.5s ease-in-out infinite;
    }

    /* ─── Tagline ────────────────────────────────────────── */
    .tagline {
        text-align: center;
        color: #a8a0cc;
        font-size: 1.15rem;
        font-weight: 300;
        margin: 0.3rem 0 1.5rem 0;
    }

    /* ─── Info Badges ────────────────────────────────────── */
    .badge-row {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-bottom: 2.5rem;
    }
    .info-badge {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 0.45rem 1.1rem;
        border-radius: 50px;
        font-size: 0.88rem;
        color: #d0cbf0;
        backdrop-filter: blur(12px);
        box-shadow: 0 2px 12px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
    }
    .info-badge:hover {
        border-color: #4ECDC4;
        box-shadow: 0 0 14px rgba(78,205,196,0.25);
        transform: translateY(-1px);
    }

    /* ─── Glass Card Mixin ───────────────────────────────── */
    .glass-card {
        background: rgba(255,255,255,0.035);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1.6rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 44px rgba(108,99,255,0.12);
    }

    /* ─── Section Headings ───────────────────────────────── */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ─── Buttons ────────────────────────────────────────── */
    .stButton>button {
        background: linear-gradient(135deg, #6C63FF 0%, #4ECDC4 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 2.4rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em;
        box-shadow: 0 4px 18px rgba(108,99,255,0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 28px rgba(78,205,196,0.45) !important;
        color: #ffffff !important;
    }
    .stButton>button:active {
        transform: translateY(0) scale(0.98) !important;
    }

    .stDownloadButton>button {
        background: linear-gradient(135deg, #4ECDC4 0%, #2ecc71 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.6rem 2.4rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 18px rgba(46,204,113,0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 28px rgba(46,204,113,0.5) !important;
        color: #ffffff !important;
    }

    /* ─── File Uploader ──────────────────────────────────── */
    [data-testid="stFileUploader"] > div {
        background: rgba(255,255,255,0.02) !important;
        border: 2px dashed rgba(108,99,255,0.4) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"] > div:hover {
        border-color: #4ECDC4 !important;
        background: rgba(78,205,196,0.03) !important;
        box-shadow: 0 0 24px rgba(78,205,196,0.08) !important;
    }

    /* ─── Metric Cards ───────────────────────────────────── */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #6C63FF, #4ECDC4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    div[data-testid="stMetricLabel"] {
        color: #a8a0cc !important;
        font-weight: 500 !important;
    }

    /* ─── Stat Cards Row ─────────────────────────────────── */
    .stat-card {
        background: rgba(255,255,255,0.035);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        transition: transform 0.3s ease;
    }
    .stat-card:hover { transform: translateY(-2px); }
    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6C63FF, #4ECDC4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .stat-label {
        color: #a8a0cc;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.3rem;
    }

    /* ─── Text Areas ─────────────────────────────────────── */
    .stTextArea > div > div > textarea {
        background: rgba(0,0,0,0.35) !important;
        color: #e0dcf8 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        font-family: 'Inter', 'Consolas', monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.65 !important;
        padding: 1rem !important;
    }

    /* ─── Comparison Panel Tints ──────────────────────────── */
    .panel-original .stTextArea > div > div > textarea {
        border-color: rgba(255,99,132,0.25) !important;
        box-shadow: inset 0 0 30px rgba(255,99,132,0.03) !important;
    }
    .panel-protected .stTextArea > div > div > textarea {
        border-color: rgba(78,205,196,0.25) !important;
        box-shadow: inset 0 0 30px rgba(78,205,196,0.03) !important;
    }

    /* ─── Expander ───────────────────────────────────────── */
    .stExpander {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
    }

    /* ─── Tabs ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        color: #a8a0cc !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(108,99,255,0.15) !important;
        border-color: #6C63FF !important;
        color: #ffffff !important;
    }

    /* ─── Scrollbars ─────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(0,0,0,0.15); border-radius: 3px; }
    ::-webkit-scrollbar-thumb { background: rgba(108,99,255,0.4); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(78,205,196,0.7); }

    /* ─── Success / Error ────────────────────────────────── */
    .stSuccess {
        background: rgba(46,204,113,0.08) !important;
        border: 1px solid rgba(46,204,113,0.25) !important;
        box-shadow: 0 0 20px rgba(46,204,113,0.1) !important;
        border-radius: 14px !important;
    }
    .stAlert {
        border-radius: 14px !important;
    }

    /* ─── Divider ────────────────────────────────────────── */
    hr {
        border-top: 1px solid rgba(255,255,255,0.06) !important;
        margin: 2.5rem 0 !important;
    }

    /* ─── Sidebar ────────────────────────────────────────── */
    div[data-testid="stSidebar"] {
        background: rgba(10,10,30,0.95) !important;
        backdrop-filter: blur(20px);
    }
    .sidebar-badge {
        background: rgba(108,99,255,0.12);
        border: 1px solid rgba(108,99,255,0.25);
        border-radius: 10px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.5rem;
        text-align: center;
        color: #d0cbf0;
        font-size: 0.88rem;
        font-weight: 500;
    }

    /* ─── Footer ─────────────────────────────────────────── */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.3);
        font-size: 0.78rem;
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(255,255,255,0.04);
    }
    .footer a { color: rgba(108,99,255,0.6); text-decoration: none; }

    /* ─── Float-in Animation ─────────────────────────────── */
    @keyframes floatIn {
        0%   { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .float-in { animation: floatIn 0.6s ease-out forwards; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Session State ───────────────────────────────────────────────
for key, default in {
    "file_content": None,
    "file_name": None,
    "file_type": None,
    "redaction_result": None,
    "is_redacted": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Helper: Load a sample document from disk ────────────────────
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_documents")


@st.cache_data(show_spinner=False)
def load_sample(filename: str) -> str:
    """Read a sample file from the sample_documents directory."""
    filepath = os.path.join(SAMPLE_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def _set_sample(filename: str, content: str):
    """Store sample document into session state."""
    st.session_state.file_content = content
    st.session_state.file_name = filename
    st.session_state.file_type = filename.rsplit(".", 1)[-1].lower()
    st.session_state.is_redacted = False
    st.session_state.redaction_result = None


# ================================================================
#  HEADER
# ================================================================
st.markdown(
    """
    <div style="text-align:center; margin-top:1.5rem;" class="float-in">
        <span class="shield-icon">🛡️</span>
        <div class="main-title">MedShield</div>
        <p class="tagline">Protect sensitive information in medical documents — locally &amp; securely</p>
        <div class="badge-row">
            <span class="info-badge">🔒 100% Local</span>
            <span class="info-badge">🚀 Instant Processing</span>
            <span class="info-badge">📄 TXT · CSV · PDF</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================================================================
#  PRIVACY & DISCLAIMER
# ================================================================
with st.expander("⚠️ Privacy & Disclaimer", expanded=False):
    st.markdown(
        """
**🔒 Privacy Notice**
All files are processed **locally** on your machine. No data is uploaded to
external servers or third-party APIs. Do **not** upload files you do not trust
this application with.

**⚖️ Disclaimer**
MedShield is a **document-redaction tool** designed to assist with privacy
protection. It is **NOT**:
- A guarantee of legal compliance (HIPAA, GDPR, etc.)
- A medical diagnosis tool
- A substitute for professional legal or medical advice

Always verify redactions manually before sharing protected documents.
"""
    )

# ================================================================
#  FILE UPLOAD
# ================================================================
st.markdown('<p class="section-title">📤 Upload Your Document</p>', unsafe_allow_html=True)

upload_col, sample_col = st.columns([2.5, 1], gap="large")

with upload_col:
    uploaded_file = st.file_uploader(
        "Drop your medical document here",
        type=["txt", "csv", "pdf"],
        help=f"Accepted formats: TXT, CSV, PDF · Max size: {MAX_FILE_SIZE_MB} MB",
    )

with sample_col:
    st.markdown("**Or try a sample:**")
    if st.button("📋 Medical Report", use_container_width=True, key="btn_sample1"):
        _set_sample("sample_medical_report.txt", load_sample("sample_medical_report.txt"))
        st.rerun()
    if st.button("📊 Patient Records", use_container_width=True, key="btn_sample2"):
        _set_sample("sample_patient_records.csv", load_sample("sample_patient_records.csv"))
        st.rerun()
    if st.button("🧪 Lab Report", use_container_width=True, key="btn_sample3"):
        _set_sample("sample_lab_report.txt", load_sample("sample_lab_report.txt"))
        st.rerun()

# ── Handle uploaded file ────────────────────────────────────────
if uploaded_file is not None:
    success, content_or_error, file_type = process_file(uploaded_file)
    if success:
        st.session_state.file_content = content_or_error
        st.session_state.file_name = uploaded_file.name
        st.session_state.file_type = file_type
        st.session_state.is_redacted = False
        st.session_state.redaction_result = None
    else:
        st.error(f"❌ {content_or_error}")

# ================================================================
#  DOCUMENT PREVIEW + PROTECT BUTTON
# ================================================================
if st.session_state.file_content:
    st.divider()

    content = st.session_state.file_content

    # ── File info metrics ───────────────────────────────────────
    st.markdown(
        f"""
        <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;" class="float-in">
            <div class="stat-card" style="flex:1; min-width:140px;">
                <div class="stat-number">📄</div>
                <div class="stat-label">{st.session_state.file_name}</div>
            </div>
            <div class="stat-card" style="flex:1; min-width:140px;">
                <div class="stat-number">{len(content):,}</div>
                <div class="stat-label">Characters</div>
            </div>
            <div class="stat-card" style="flex:1; min-width:140px;">
                <div class="stat-number">{len(content.splitlines()):,}</div>
                <div class="stat-label">Lines</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Show preview only when NOT redacted yet ─────────────────
    if not st.session_state.is_redacted:
        st.markdown('<p class="section-title">📋 Document Preview</p>', unsafe_allow_html=True)
        st.text_area(
            "Document content preview",
            content,
            height=300,
            disabled=True,
            label_visibility="collapsed",
        )

        # ── Big PROTECT button ──────────────────────────────────
        st.markdown("")  # spacer
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            if st.button("🛡️  Protect Document", use_container_width=True, key="btn_protect"):
                with st.spinner("🔍 Scanning for sensitive information…"):
                    time.sleep(0.8)  # brief delay for visual feedback
                    result = redact_text(content)
                    st.session_state.redaction_result = result
                    st.session_state.is_redacted = True
                    st.rerun()

# ================================================================
#  RESULTS — shown after redaction
# ================================================================
if st.session_state.is_redacted and st.session_state.redaction_result:
    result: RedactionResult = st.session_state.redaction_result

    st.success("✅ Document successfully protected!")

    # ── Redaction Summary ───────────────────────────────────────
    st.markdown('<p class="section-title">📊 Redaction Summary</p>', unsafe_allow_html=True)

    if result.redaction_count == 0:
        st.info("ℹ️ No sensitive information was detected in this document.")
    else:
        # Build stat cards with HTML for premium look
        detail_items = result.redaction_details  # Dict[str, int]
        num_categories = len(detail_items)

        # Top-level metrics
        st.markdown(
            f"""
            <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;" class="float-in">
                <div class="stat-card" style="flex:1; min-width:160px;">
                    <div class="stat-number">{result.redaction_count}</div>
                    <div class="stat-label">Total Items Redacted</div>
                </div>
                <div class="stat-card" style="flex:1; min-width:160px;">
                    <div class="stat-number">{num_categories}</div>
                    <div class="stat-label">Categories Detected</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Per-category breakdown
        cat_cards_html = ""
        cat_icons = {
            "PHONE": "📱", "EMAIL": "📧", "AADHAAR": "🪪", "SSN": "🔢",
            "DOB": "🎂", "DATE": "📅", "MRN": "🏥", "NAME": "👤",
            "ADDRESS": "📍", "PINCODE": "📮", "INSURANCE_ID": "💳",
        }
        for cat, count in detail_items.items():
            icon = cat_icons.get(cat, "🔒")
            cat_cards_html += f"""
            <div class="stat-card" style="flex:1; min-width:120px;">
                <div class="stat-number">{icon} {count}</div>
                <div class="stat-label">{cat.replace('_', ' ')}</div>
            </div>
            """
        st.markdown(
            f'<div style="display:flex; gap:0.8rem; flex-wrap:wrap;" class="float-in">{cat_cards_html}</div>',
            unsafe_allow_html=True,
        )

    # ── Side-by-Side Comparison ─────────────────────────────────
    st.divider()
    st.markdown('<p class="section-title">🔍 Comparison</p>', unsafe_allow_html=True)

    col_orig, col_prot = st.columns(2, gap="medium")

    with col_orig:
        st.markdown(
            '<div class="panel-original">'
            '<p style="color:#ff6384; font-weight:600; font-size:1rem;">📄 Original Document</p>',
            unsafe_allow_html=True,
        )
        st.text_area(
            "Original",
            st.session_state.file_content,
            height=420,
            disabled=True,
            label_visibility="collapsed",
            key="ta_original",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_prot:
        st.markdown(
            '<div class="panel-protected">'
            '<p style="color:#4ECDC4; font-weight:600; font-size:1rem;">🛡️ Protected Document</p>',
            unsafe_allow_html=True,
        )
        st.text_area(
            "Protected",
            result.redacted_text,
            height=420,
            disabled=True,
            label_visibility="collapsed",
            key="ta_protected",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Download ────────────────────────────────────────────────
    st.divider()
    st.markdown('<p class="section-title">💾 Save Protected File</p>', unsafe_allow_html=True)

    file_bytes, suggested_name = create_download_content(
        result.redacted_text, st.session_state.file_name
    )

    _, dl_col, _ = st.columns([1, 2, 1])
    with dl_col:
        st.download_button(
            label=f"⬇️  Download {suggested_name}",
            data=file_bytes,
            file_name=suggested_name,
            mime="text/plain",
            use_container_width=True,
            key="btn_download",
        )

# ================================================================
#  SIDEBAR — What MedShield Detects
# ================================================================
with st.sidebar:
    st.markdown("### 🔍 What MedShield Detects")
    st.markdown("We scan for these types of sensitive information:")
    st.markdown("")

    patterns = get_supported_patterns()
    sidebar_icons = {
        "DOB": "🎂", "NAME": "👤", "ADDRESS": "📍", "PINCODE": "📮",
        "MRN": "🏥", "INSURANCE_ID": "💳", "PHONE": "📱", "EMAIL": "📧",
        "AADHAAR": "🪪", "SSN": "🔢", "DATE": "📅",
    }
    for pat in patterns:
        icon = sidebar_icons.get(pat, "🔒")
        st.markdown(
            f'<div class="sidebar-badge">{icon} {pat.replace("_", " ")}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        f"**Supported files:** {', '.join(ALLOWED_EXTENSIONS)}  \n"
        f"**Max file size:** {MAX_FILE_SIZE_MB} MB"
    )

# ================================================================
#  FOOTER
# ================================================================
st.markdown(
    """
    <div class="footer">
        <strong>MedShield v1.0</strong> · Built with ❤️ for healthcare privacy<br>
        <small>This tool is for document redaction only. Not a medical or legal compliance tool.
        Always verify redactions before sharing.</small>
    </div>
    """,
    unsafe_allow_html=True,
)
