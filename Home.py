"""
IEP Parent Guide — Home
Upload one or multiple SOP PDFs here. Everything flows from this page.
"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="IEP Parent Guide",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.rag_engine import init_session, load_pdf_to_session, auto_load_from_docs, clear_all_docs
from utils.theme import apply_theme, sidebar_brand, page_header

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

# ── Hero ──────────────────────────────────────────────────────────────────────
page_header(
    "📚",
    "IEP Parent Guide",
    "Upload your IEP Standard Operating Procedures document — we turn it into plain-English answers, visual guides and checklists",
    "#1E3A8A",
)

# ── Upload section ────────────────────────────────────────────────────────────
if not st.session_state.pdf_loaded:
    st.markdown("""
    <div style="background:white;border:2px dashed #93C5FD;border-radius:16px;
                padding:32px;text-align:center;margin-bottom:24px;">
        <div style="font-size:3rem;margin-bottom:12px;">📄</div>
        <div style="font-family:'Nunito',sans-serif;font-weight:800;font-size:1.2rem;
                    color:#1E3A8A;margin-bottom:8px;">
            Upload Your IEP SOP Document(s)
        </div>
        <div style="color:#64748B;font-size:0.92rem;max-width:520px;margin:0 auto;">
            Upload one PDF or multiple PDFs together — for example your State SOP and the
            Federal IDEA guidelines. All documents are searched together and answers show
            which file they came from. Your files stay private and are never sent anywhere.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choose one or more IEP SOP PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can upload multiple PDFs at once. Hold Ctrl/Cmd to select more than one.",
        label_visibility="collapsed",
    )

    if uploaded_files:
        any_ok = False
        for f in uploaded_files:
            ok = load_pdf_to_session(f, f.name)
            if ok:
                any_ok = True
        if any_ok:
            total_q = sum(len(v) for v in st.session_state.pdf_questions.values())
            total_p = sum(len(d["pages"]) for d in st.session_state.docs.values())
            st.success(
                f"✅ {len(st.session_state.docs)} document(s) loaded · "
                f"{total_p} pages · {total_q} questions generated"
            )
            st.balloons()
            st.rerun()
        else:
            st.error("Could not read the PDF(s). Please check the files and try again.")

else:
    # ── Loaded state ──────────────────────────────────────────────────────────
    docs    = st.session_state.docs
    n_docs  = len(docs)
    total_p = sum(len(d["pages"])    for d in docs.values())
    total_s = sum(len(d["sections"]) for d in docs.values())
    total_q = sum(len(v) for v in st.session_state.pdf_questions.values())
    total_c = len(st.session_state.pdf_questions)

    st.markdown(f"""
    <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:14px;
                padding:18px 24px;margin-bottom:20px;">
        <div style="font-family:'Nunito',sans-serif;font-weight:800;
                    color:#15803D;font-size:1rem;margin-bottom:8px;">
            ✅ {n_docs} Document{"s" if n_docs > 1 else ""} Ready
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
    """, unsafe_allow_html=True)

    for doc_name in docs:
        dp = len(docs[doc_name]["pages"])
        st.markdown(f"""
        <span style="background:#D1FAE5;color:#065F46;border-radius:8px;
                     padding:4px 12px;font-size:0.8rem;font-weight:700;">
            📄 {doc_name} · {dp} pages
        </span>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Add more PDFs while keeping existing ones
    with st.expander("➕ Add another document"):
        more = st.file_uploader(
            "Add more PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="add_more",
        )
        if more:
            for f in more:
                load_pdf_to_session(f, f.name)
            st.rerun()

    # ── Metric row ────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Documents",     n_docs)
    with c2: st.metric("Pages Read",    total_p)
    with c3: st.metric("Sections Found",total_s)
    with c4: st.metric("Questions",     total_q)
    with c5: st.metric("Topic Areas",   total_c)

    st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)

    # ── Module cards ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                font-size:1.1rem;color:#1E293B;margin:20px 0 12px;">
        What you can explore
    </div>
    """, unsafe_allow_html=True)

    row1 = st.columns(3)
    row2 = st.columns(3)
    features = [
        ("❓", "Ask a Question",
         "Click any auto-generated question or type your own. Answers come from ALL your uploaded documents, grouped by file with page numbers.",
         "#2563EB"),
        ("🗺️", "Process Flowchart",
         "See the entire IEP journey as a visual step-by-step map. Click any step to read what your documents say about it.",
         "#0D9488"),
        ("📋", "Cheat Sheet",
         "Every section of your documents explained in plain English. One card per topic. No jargon.",
         "#7C3AED"),
        ("⏱️", "My Timeline",
         "Enter the date you signed consent. See your 60-day deadline, where you are today, and what should happen next.",
         "#D97706"),
        ("🛡️", "My Rights",
         "Every parent right explained in plain language — what it means, what to say, what to do if the school refuses.",
         "#DC2626"),
        ("📖", "Glossary",
         "Every IEP abbreviation and term explained simply. No more confusion over IEP, LRE, PWN, FBA, ESY and more.",
         "#16A34A"),
    ]
    all_cols = list(row1) + list(row2)
    for col, (icon, title, desc, color) in zip(all_cols, features):
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:14px;border:1px solid #E2E8F0;
                        border-top:4px solid {color};padding:20px 18px;
                        margin-bottom:12px;min-height:160px;">
                <div style="font-size:1.6rem;margin-bottom:8px;">{icon}</div>
                <div style="font-family:'Nunito',sans-serif;font-weight:800;
                            color:#1E293B;font-size:0.95rem;margin-bottom:6px;">{title}</div>
                <div style="color:#64748B;font-size:0.82rem;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Where to start ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                font-size:1.1rem;color:#1E293B;margin:20px 0 12px;">
        Where should I start?
    </div>
    """, unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    for col, (icon, title, desc, bg, fg) in zip([s1, s2, s3], [
        ("🆕","Just getting started",
         "Go to → Process Flowchart to see the big picture, then → Ask Questions to understand what happens first.",
         "#EFF6FF","#1E40AF"),
        ("📅","Have a meeting coming up",
         "Go to → My Timeline to check your 60-day deadline, then → My Rights to know what to ask for at the meeting.",
         "#FFF7ED","#92400E"),
        ("❓","Something feels wrong",
         "Go to → My Rights to understand what the school must do, then → Ask Questions about your specific concern.",
         "#FFF1F2","#9F1239"),
    ]):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border-radius:12px;padding:16px 18px;
                        border:1px solid {fg}33;">
                <div style="font-size:1.4rem;margin-bottom:6px;">{icon}</div>
                <div style="font-family:'Nunito',sans-serif;font-weight:800;
                            color:{fg};font-size:0.9rem;margin-bottom:6px;">{title}</div>
                <div style="color:{fg}cc;font-size:0.82rem;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Clear all ─────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    c_left, c_right = st.columns([3, 1])
    with c_left:
        st.markdown("""
        <div style="color:#94A3B8;font-size:0.82rem;padding-top:8px;">
            Want to start over with different documents? Clear everything and upload new PDFs.
        </div>
        """, unsafe_allow_html=True)
    with c_right:
        if st.button("🗑️  Clear All Documents", use_container_width=True):
            clear_all_docs()
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#94A3B8;font-size:0.75rem;
            margin-top:40px;padding-top:16px;border-top:1px solid #E2E8F0;">
    IEP Parent Guide · All answers come from your uploaded documents ·
    Based on IDEA Federal Guidelines · Free to use
</div>
""", unsafe_allow_html=True)
