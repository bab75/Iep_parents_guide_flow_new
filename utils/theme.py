"""
IEP Parent App — Shared Theme
Warm, accessible, parent-friendly design.
"""
import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@400;600&display=swap');

    :root {
        --primary:  #2563EB;
        --teal:     #0D9488;
        --amber:    #D97706;
        --rose:     #DC2626;
        --green:    #16A34A;
        --purple:   #7C3AED;
        --bg:       #F8FAFF;
        --card:     #FFFFFF;
        --border:   #E2E8F0;
        --text:     #1E293B;
        --muted:    #64748B;
        --sans:     'Nunito', sans-serif;
        --body:     'Nunito Sans', sans-serif;
    }

    html, body, [class*="css"] {
        font-family: var(--body) !important;
        color: var(--text);
    }

    .stApp { background: var(--bg) !important; }

    .main .block-container {
        padding: 1.5rem 2rem 3rem !important;
        max-width: 1100px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A8A 0%, #1D4ED8 100%) !important;
    }
    [data-testid="stSidebar"] * { color: #DBEAFE !important; }
    [data-testid="stSidebarNav"] a {
        font-family: var(--sans) !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        margin: 2px 6px !important;
        transition: all 0.2s !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(255,255,255,0.15) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(255,255,255,0.2) !important;
        border-left: 3px solid #FCD34D !important;
        color: white !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        font-family: var(--sans) !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #1D4ED8 !important;
        transform: translateY(-1px) !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid var(--border) !important;
        font-family: var(--body) !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid var(--border) !important;
        font-family: var(--body) !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        font-family: var(--sans) !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        background: white !important;
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
    }
    .streamlit-expanderContent {
        background: #FAFCFF !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 5px !important;
        border: 1px solid var(--border) !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--sans) !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
        padding: 9px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
        border: 1px solid var(--border) !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div > div > div {
        background: var(--teal) !important;
    }

    /* ── Hide branding ── */
    #MainMenu, footer, header { visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)


def sidebar_brand():
    with st.sidebar:
        st.markdown("""
        <div style="padding:16px 10px 24px;">
            <div style="font-size:1.6rem;margin-bottom:6px;">📚</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:900;
                        font-size:1.1rem;color:white;line-height:1.2;">
                IEP Guide<br>
                <span style="font-weight:600;font-size:0.85rem;
                             color:rgba(255,255,255,0.7);">for Parents & Families</span>
            </div>
            <div style="width:30px;height:3px;background:#FCD34D;
                        border-radius:2px;margin-top:10px;"></div>
        </div>
        """, unsafe_allow_html=True)


def page_header(emoji: str, title: str, subtitle: str, color: str = "#2563EB"):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{color} 0%,{color}cc 100%);
                border-radius:16px;padding:28px 32px;margin-bottom:24px;
                position:relative;overflow:hidden;">
        <div style="position:absolute;top:-30px;right:-30px;width:160px;height:160px;
                    background:rgba(255,255,255,0.06);border-radius:50%;"></div>
        <div style="position:relative;z-index:1;">
            <div style="font-size:2.2rem;margin-bottom:8px;">{emoji}</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:900;
                        font-size:1.7rem;color:white;line-height:1.2;
                        margin-bottom:6px;">{title}</div>
            <div style="color:rgba(255,255,255,0.85);font-size:0.95rem;">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def status_banner():
    """Show PDF load status — works for single or multiple documents."""
    if st.session_state.get("pdf_loaded"):
        docs   = st.session_state.get("docs", {})
        n_docs = len(docs)
        pages  = sum(len(d["pages"])    for d in docs.values())
        secs   = sum(len(d["sections"]) for d in docs.values())
        qs     = sum(len(v) for v in st.session_state.get("pdf_questions", {}).values())
        doc_label = list(docs.keys())[0] if n_docs == 1 else f"{n_docs} documents"
        doc_word = "documents" if n_docs > 1 else "document"
        st.markdown(f"""
        <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:10px;
                    padding:10px 18px;margin-bottom:16px;display:flex;
                    align-items:center;gap:12px;flex-wrap:wrap;">
            <span style="font-size:1.2rem;">✅</span>
            <div style="font-size:0.88rem;">
                <span style="font-weight:700;color:#15803D;">{n_docs} {doc_word} loaded:</span>
                <span style="color:#166534;"> {doc_label}</span>
                <span style="color:#4ADE80;"> · </span>
                <span style="color:#166534;">{pages} pages · {secs} sections · {qs} questions generated</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("📄 No document loaded yet. Go to **Home** to upload your IEP SOP PDF.")


def answer_card(result: dict, query: str, rank: int):
    """Render a single search result card — used by Flowchart, My Rights, Glossary."""
    from utils.rag_engine import highlight
    hl        = highlight(result["text"], query)
    is_first  = (rank == 1)
    border    = "2px solid #2563EB" if is_first else "1px solid #E2E8F0"
    bg        = "#EFF6FF" if is_first else "white"
    rank_lbl  = "⭐ Best Match" if is_first else f"Match {rank}"
    page_num  = result["page"]
    section   = result["section"][:40] + ("…" if len(result["section"]) > 40 else "")
    category  = result["category"]
    st.markdown(
        f'''<div style="background:{bg};border:{border};border-radius:12px;
                    padding:16px 20px;margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:6px;">
                <span style="font-weight:700;color:#1E40AF;font-size:0.85rem;
                             font-family:Nunito,sans-serif;">{rank_lbl}</span>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <span style="background:#DBEAFE;color:#1E40AF;border-radius:6px;
                                 padding:2px 10px;font-size:0.75rem;font-weight:700;">
                        Page {page_num}</span>
                    <span style="background:#F0FDF4;color:#15803D;border-radius:6px;
                                 padding:2px 10px;font-size:0.75rem;font-weight:700;">
                        {section}</span>
                    <span style="background:#F5F3FF;color:#6D28D9;border-radius:6px;
                                 padding:2px 10px;font-size:0.75rem;font-weight:700;">
                        {category}</span>
                </div>
            </div>
            <div style="font-size:0.9rem;line-height:1.85;color:#334155;">{hl}</div>
        </div>''',
        unsafe_allow_html=True,
    )
