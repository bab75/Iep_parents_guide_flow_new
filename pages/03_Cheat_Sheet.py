"""
Page: Cheat Sheet
Every section of the PDF shown as a plain-English card.
Content pulled directly from the uploaded document.
"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Cheat Sheet · IEP Guide", page_icon="📋", layout="wide")

from utils.rag_engine import init_session, auto_load_from_docs, search_chunks, SECTION_CATEGORIES
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

page_header("📋", "Cheat Sheet",
            "Every topic from your document in plain English — no jargon, no page-flipping",
            "#7C3AED")
status_banner()

if not st.session_state.pdf_loaded:
    st.stop()

questions = st.session_state.pdf_questions
chunks    = st.session_state.get("all_chunks", [])
sections  = []

# ── Category color map ────────────────────────────────────────────────────────
CAT_COLORS = {
    "Getting Started":  "#2563EB",
    "Timelines":        "#D97706",
    "Evaluation":       "#7C3AED",
    "Eligibility":      "#0D9488",
    "The IEP Document": "#1D4ED8",
    "Placement":        "#16A34A",
    "Parent Rights":    "#DC2626",
    "Meetings":         "#0891B2",
    "Disagreements":    "#B45309",
    "Special Topics":   "#9333EA",
    "General Information": "#475569",
}

# ── Filter bar ────────────────────────────────────────────────────────────────
filter_cat = st.selectbox(
    "Show topic",
    ["All Topics"] + list(questions.keys()),
    label_visibility="visible",
)
search_filter = st.text_input(
    "Search within cheat sheet",
    placeholder="e.g. consent, timeline, rights…",
    label_visibility="collapsed",
)

st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

# ── Build cheat sheet cards from questions + PDF content ─────────────────────
display_cats = list(questions.keys()) if filter_cat == "All Topics" else [filter_cat]

for cat in display_cats:
    cat_qs = questions.get(cat, [])
    if not cat_qs:
        continue

    color = CAT_COLORS.get(cat, "#475569")

    # Filter by search text
    if search_filter:
        sf = search_filter.lower()
        cat_qs = [q for q in cat_qs if sf in q["question"].lower()]
    if not cat_qs:
        continue

    # Category header
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;
                margin:20px 0 12px;padding-bottom:8px;
                border-bottom:2px solid {color}40;">
        <div style="width:14px;height:14px;border-radius:50%;
                    background:{color};flex-shrink:0;"></div>
        <div style="font-family:'Nunito',sans-serif;font-weight:900;
                    color:{color};font-size:1rem;">{cat}</div>
        <div style="font-size:0.78rem;color:#94A3B8;font-weight:600;">
            {len(cat_qs)} topic{"s" if len(cat_qs)!=1 else ""} from your document
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Grid of cards — 2 per row
    pairs = [cat_qs[i:i+2] for i in range(0, len(cat_qs), 2)]
    for pair in pairs:
        cols = st.columns(len(pair))
        for col, q_item in zip(cols, pair):
            q_text = q_item["question"]
            pg     = q_item["page"]
            sec    = q_item["section"]

            # Get best matching chunk for this question
            cache_key = f"cs_{q_text[:30]}"
            if cache_key not in st.session_state:
                results = search_chunks(chunks, q_text, top_k=1)
                st.session_state[cache_key] = results

            results = st.session_state[cache_key]
            best    = results[0] if results else None

            with col:
                # Card header
                st.markdown(f"""
                <div style="background:{color}0D;border:1px solid {color}30;
                            border-top:3px solid {color};border-radius:12px;
                            padding:16px 18px;margin-bottom:4px;">
                    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                                color:{color};font-size:0.88rem;margin-bottom:8px;">
                        {q_text}
                    </div>
                """, unsafe_allow_html=True)

                if best:
                    # Show first 300 chars of best passage
                    text = best["text"]
                    preview = text[:280] + ("…" if len(text) > 280 else "")
                    pg_num  = best["page"]
                    st.markdown(f"""
                    <div style="color:#374151;font-size:0.85rem;line-height:1.75;
                                margin-bottom:10px;">{preview}</div>
                    <div style="display:flex;gap:6px;flex-wrap:wrap;">
                        <span style="background:{color}18;color:{color};
                                     border-radius:6px;padding:2px 9px;
                                     font-size:0.72rem;font-weight:700;">
                            📄 Page {pg_num}</span>
                        <span style="background:#F1F5F9;color:#475569;
                                     border-radius:6px;padding:2px 9px;
                                     font-size:0.72rem;font-weight:600;">
                            {sec[:35]}{'…' if len(sec)>35 else ''}</span>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="color:#94A3B8;font-size:0.82rem;font-style:italic;">
                        See page {pg} of your document for information on this topic.
                    </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Expand button to see more
                with st.expander("Read full passage from document"):
                    full_results = search_chunks(chunks, q_text, top_k=2)
                    if full_results:
                        for r in full_results:
                            st.markdown(f"""
                            <div style="background:#F8FAFF;border-radius:8px;
                                        padding:12px 14px;margin-bottom:8px;
                                        font-size:0.87rem;line-height:1.8;color:#334155;
                                        border-left:3px solid {color};">
                                <div style="font-size:0.72rem;font-weight:700;
                                            color:{color};margin-bottom:6px;">
                                    📄 Page {r['page']} · {r['section'][:40]}</div>
                                {r['text'][:600]}{"…" if len(r['text'])>600 else ""}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No passage found for this topic in your document.")

# ── Download cheat sheet as text ──────────────────────────────────────────────
if st.button("Download Cheat Sheet as Text File", use_container_width=False):
    lines = ["IEP CHEAT SHEET\n", "=" * 40 + "\n"]
    for cat in display_cats:
        lines.append(f"\n{cat.upper()}\n{'-'*len(cat)}\n")
        for q_item in questions.get(cat, []):
            q_text = q_item["question"]
            cache_key = f"cs_{q_text[:30]}"
            results = st.session_state.get(cache_key, [])
            lines.append(f"\n{q_text}\n")
            if results:
                lines.append(f"Page {results[0]['page']}: {results[0]['text'][:300]}…\n")
    content = "\n".join(lines)
    st.download_button(
        "⬇️ Save Cheat Sheet",
        content,
        file_name="IEP_CheatSheet.txt",
        mime="text/plain",
    )
