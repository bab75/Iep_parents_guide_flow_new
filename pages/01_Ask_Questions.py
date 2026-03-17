"""
Page: Ask a Question  (v2)
- Questions auto-generated from every uploaded PDF
- Answers grouped by document when multiple PDFs loaded
- Each answer: plain-English summary → key bullet points → action line → raw text toggle
- Clear all documents button at bottom of left panel
"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Ask a Question · IEP Guide", page_icon="❓", layout="wide")

from utils.rag_engine import (
    init_session, auto_load_from_docs,
    search_all_chunks, group_by_doc, get_related,
    get_plain_answer, get_action_line, extract_bullets,
    highlight, clear_all_docs,
)
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

page_header(
    "❓", "Ask a Question",
    "Click any question — or type your own. Every answer comes from your uploaded document with the page number.",
    "#2563EB",
)
status_banner()

if not st.session_state.pdf_loaded:
    st.stop()

questions   = st.session_state.pdf_questions
loaded_docs = list(st.session_state.docs.keys())

# ────────────────────────────────────────────────────────────────────────────
# RICH ANSWER CARD
# ────────────────────────────────────────────────────────────────────────────
def render_answer_card(result: dict, query: str, rank: int, total_docs: int):
    """Structured answer card — no nested quotes in f-strings."""
    doc_name  = result.get("doc_name", "")
    page_num  = result["page"]
    section   = result["section"]
    sec_short = section[:45] + ("…" if len(section) > 45 else "")
    category  = result["category"]
    raw_text  = result["text"]
    is_best   = (rank == 1)
    star      = "⭐ Best Match" if is_best else "Match " + str(rank)
    border    = "2px solid #2563EB" if is_best else "1px solid #E2E8F0"
    bg        = "#EFF6FF" if is_best else "white"

    plain_ans = get_plain_answer(query)
    action    = get_action_line(query)
    bullets   = extract_bullets(raw_text, max_bullets=3)
    hl_text   = highlight(raw_text, query, max_chars=400)

    # Fallback: always show a plain English intro if no template matched
    if not plain_ans and is_best:
        plain_ans = (
            "Your document has information about this topic in the "
            + section + " section (Page " + str(page_num) + "). "
            "The key points from that section are shown below."
        )

    # ── Doc badge (only when multiple docs loaded) ────────────────────────────
    doc_badge = ""
    if total_docs > 1 and doc_name:
        doc_badge = (
            '<span style="background:#FEE2E2;color:#991B1B;border-radius:8px;'
            'padding:3px 10px;font-size:11px;font-weight:700;">📂 '
            + doc_name + "</span>"
        )

    # ── Badge row HTML ────────────────────────────────────────────────────────
    badge_row = (
        '<div style="display:flex;gap:6px;flex-wrap:wrap;'
        'align-items:center;margin-bottom:14px;">'
        + '<span style="background:#FEF9C3;color:#854D0E;border-radius:8px;'
        'padding:3px 10px;font-size:11px;font-weight:700;">' + star + "</span>"
        + '<span style="background:#DBEAFE;color:#1E40AF;border-radius:8px;'
        'padding:3px 10px;font-size:11px;font-weight:700;">📄 Page '
        + str(page_num) + "</span>"
        + '<span style="background:#D1FAE5;color:#065F46;border-radius:8px;'
        'padding:3px 10px;font-size:11px;font-weight:700;">'
        + sec_short + "</span>"
        + '<span style="background:#EDE9FE;color:#5B21B6;border-radius:8px;'
        'padding:3px 10px;font-size:11px;font-weight:700;">'
        + category + "</span>"
        + doc_badge
        + "</div>"
    )

    # ── Plain English block ───────────────────────────────────────────────────
    plain_block = ""
    if plain_ans and (is_best or total_docs > 1):
        plain_block = (
            '<div style="background:#EFF6FF;border-radius:10px;'
            'padding:13px 16px;margin-bottom:12px;">'
            '<div style="font-size:11px;font-weight:700;color:#1E40AF;'
            'text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px;">'
            "Plain English Answer</div>"
            '<div style="font-size:0.93rem;color:#1E3A8A;line-height:1.75;font-weight:500;">'
            + plain_ans + "</div></div>"
        )

    # ── Bullet points ─────────────────────────────────────────────────────────
    bullets_block = ""
    if bullets:
        items = "".join(
            '<li style="display:flex;gap:10px;align-items:flex-start;padding:6px 0;'
            'border-bottom:1px solid #E2E8F0;font-size:0.88rem;color:#374151;line-height:1.65;">'
            '<span style="width:7px;height:7px;border-radius:50%;background:#3B82F6;'
            'flex-shrink:0;margin-top:6px;"></span>'
            "<span>" + b + "</span></li>"
            for b in bullets
        )
        bullets_block = (
            '<div style="margin-bottom:12px;">'
            '<div style="font-size:11px;font-weight:700;color:#374151;'
            'text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px;">'
            "Key Points from Your Document</div>"
            '<ul style="list-style:none;padding:0;margin:0;border-top:1px solid #E2E8F0;">'
            + items + "</ul></div>"
        )

    # ── Action line ───────────────────────────────────────────────────────────
    action_block = ""
    if action and is_best:
        action_block = (
            '<div style="background:#F0FDF4;border-radius:8px;'
            'padding:10px 14px;margin-bottom:12px;">'
            '<div style="font-size:11px;font-weight:700;color:#15803D;'
            'text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px;">'
            "What This Means for You</div>"
            '<div style="font-size:0.88rem;color:#166534;font-weight:600;line-height:1.65;">'
            "✅ " + action + "</div></div>"
        )

    # ── Assemble and render card ──────────────────────────────────────────────
    card_html = (
        '<div style="background:' + bg + ';border:' + border + ';'
        + 'border-radius:14px;padding:18px 22px;margin-bottom:14px;">'
        + badge_row
        + plain_block
        + bullets_block
        + action_block
        + "</div>"
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # ── Raw text expander ─────────────────────────────────────────────────────
    with st.expander("Show exact text from document - Page " + str(page_num)):
        raw_html = (
            '<div style="background:#F8FAFF;border-left:3px solid #93C5FD;'
            + 'border-radius:6px;padding:14px 16px;font-size:0.85rem;'
            + 'line-height:1.85;color:#334155;">' + hl_text + "</div>"
        )
        st.markdown(raw_html, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# Layout
# ════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1, 2], gap="large")

# ════════════════════════════════════════════════════════════════════════════
# LEFT — document status + question list + clear button
# ════════════════════════════════════════════════════════════════════════════
with left:

    # Loaded documents summary
    st.markdown(f"""
    <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:10px;
                padding:12px 16px;margin-bottom:14px;">
        <div style="font-weight:700;color:#15803D;font-size:0.85rem;margin-bottom:4px;">
            Documents loaded ({len(loaded_docs)})
        </div>
    """, unsafe_allow_html=True)

    for doc in loaded_docs:
        doc_data = st.session_state.docs[doc]
        n_pages  = len(doc_data["pages"])
        n_chunks = len(doc_data["chunks"])
        c_left, c_right = st.columns([5, 1])
        with c_left:
            st.markdown(f"""
            <div style="font-size:0.8rem;color:#166534;padding:2px 0;">
                📄 <b>{doc}</b><br>
                <span style="color:#4ADE80;font-size:0.72rem;">
                    {n_pages} pages · {n_chunks} sections indexed</span>
            </div>
            """, unsafe_allow_html=True)
        with c_right:
            if st.button("✕", key=f"rm_{doc[:15]}", help=f"Remove {doc}"):
                from utils.rag_engine import remove_doc
                remove_doc(doc)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Category filter
    st.markdown("""
    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                color:#1E293B;font-size:0.92rem;margin:12px 0 6px;">
        Questions from your documents
    </div>
    """, unsafe_allow_html=True)

    all_cats      = list(questions.keys())
    selected_cat  = st.selectbox("Topic area", ["All Topics"] + all_cats,
                                  label_visibility="visible")
    display_cats  = all_cats if selected_cat == "All Topics" else [selected_cat]

    cat_colors = {
        "Getting Started": "#2563EB", "Timelines": "#D97706",
        "Evaluation": "#7C3AED",      "Eligibility": "#0D9488",
        "The IEP Document": "#1D4ED8","Placement": "#16A34A",
        "Parent Rights": "#DC2626",   "Meetings": "#0891B2",
        "Disagreements": "#B45309",   "Special Topics": "#9333EA",
        "General Information": "#475569",
    }

    for cat in display_cats:
        cat_qs = questions.get(cat, [])
        if not cat_qs:
            continue
        c = cat_colors.get(cat, "#475569")
        st.markdown(f"""
        <div style="font-size:0.72rem;font-weight:800;color:{c};
                    text-transform:uppercase;letter-spacing:.06em;
                    margin:12px 0 5px;">{cat}</div>
        """, unsafe_allow_html=True)

        for q_item in cat_qs:
            q_text = q_item["question"]
            if st.button(q_text, key=f"q_{q_text[:28]}", use_container_width=True):
                results = search_all_chunks(q_text, top_k=6)
                st.session_state.active_q          = q_text
                st.session_state.active_cat        = cat
                st.session_state.search_results    = results
                st.session_state.history.insert(0, {
                    "question": q_text, "results": results, "category": cat
                })
                st.rerun()

    # ── CLEAR ALL BUTTON ──────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">
        Remove all documents and start over
    </div>
    """, unsafe_allow_html=True)
    if st.button("🗑️  Clear All Documents", use_container_width=True, type="secondary"):
        clear_all_docs()
        st.success("All documents cleared. Go to Home to upload new ones.")
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# RIGHT — search bar + rich answer display
# ════════════════════════════════════════════════════════════════════════════
with right:

    st.markdown("""
    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                color:#1E293B;font-size:0.95rem;margin-bottom:8px;">
        Or type your own question
    </div>
    """, unsafe_allow_html=True)

    # Reset input value when clear was clicked
    if st.session_state.get("_clear_input"):
        st.session_state["_clear_input"] = False
        default_val = ""
    else:
        default_val = st.session_state.get("_query_val", "")

    query = st.text_input(
        "Your question",
        value=default_val,
        placeholder="e.g. What happens after I sign the consent form?",
        label_visibility="collapsed",
        key="free_query",
    )
    st.session_state["_query_val"] = query

    s1, s2 = st.columns([3, 1])
    with s1:
        search_btn = st.button("Search All Documents", use_container_width=True, type="primary")
    with s2:
        if st.button("Clear results", use_container_width=True):
            st.session_state.search_results = []
            st.session_state.active_q       = ""
            st.session_state.history        = []
            st.session_state["_clear_input"] = True
            st.rerun()

    if search_btn and query.strip():
        results = search_all_chunks(query, top_k=6)
        st.session_state.active_q       = query
        st.session_state.active_cat     = ""
        st.session_state.search_results = results
        st.session_state.history.insert(0, {
            "question": query, "results": results, "category": ""
        })

    # ── Active results ────────────────────────────────────────────────────────
    if st.session_state.search_results:
        active_q  = st.session_state.active_q
        results   = st.session_state.search_results
        grouped   = group_by_doc(results)
        num_docs  = len(grouped)

        # Question banner
        st.markdown(f"""
        <div style="background:#EFF6FF;border-left:4px solid #2563EB;
                    border-radius:8px;padding:12px 16px;margin:12px 0 16px;">
            <div style="font-size:11px;font-weight:700;color:#3B82F6;
                        text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px;">
                Your Question</div>
            <div style="font-weight:700;color:#1E293B;font-size:1rem;">{active_q}</div>
            <div style="color:#64748B;font-size:0.8rem;margin-top:4px;">
                {len(results)} result{"s" if len(results)!=1 else ""} across
                {num_docs} document{"s" if num_docs!=1 else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not results:
            st.info("No matching passages found. Try rephrasing or use a different keyword.")
        elif num_docs == 1:
            # Single doc — show flat list
            doc_name = list(grouped.keys())[0]
            for i, r in enumerate(results, 1):
                render_answer_card(r, active_q, i, num_docs)
        else:
            # Multiple docs — show grouped by document
            for doc_name, doc_results in grouped.items():
                st.markdown(f"""
                <div style="background:#F8FAFF;border:1px solid #BFDBFE;
                            border-radius:10px;padding:10px 16px;margin:14px 0 8px;
                            display:flex;align-items:center;gap:8px;">
                    <span style="font-size:1rem;">📂</span>
                    <div>
                        <div style="font-weight:800;color:#1E40AF;font-size:0.9rem;">
                            {doc_name}</div>
                        <div style="font-size:0.75rem;color:#64748B;">
                            {len(doc_results)} result{"s" if len(doc_results)!=1 else ""} from this document
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                for i, r in enumerate(doc_results, 1):
                    render_answer_card(r, active_q, i, num_docs)

        # ── Related questions ─────────────────────────────────────────────────
        cat     = st.session_state.active_cat
        related = get_related(active_q, questions, cat) if cat else []
        if related:
            st.markdown("""
            <div style="font-family:'Nunito',sans-serif;font-weight:800;
                        color:#1E293B;font-size:0.88rem;margin:18px 0 8px;">
                You might also want to know:
            </div>
            """, unsafe_allow_html=True)
            for rq in related:
                if st.button(f"→  {rq['question']}", key=f"rq_{rq['question'][:22]}"):
                    res = search_all_chunks(rq["question"], top_k=6)
                    st.session_state.active_q       = rq["question"]
                    st.session_state.active_cat     = cat
                    st.session_state.search_results = res
                    st.session_state.history.insert(0, {
                        "question": rq["question"], "results": res, "category": cat
                    })
                    st.rerun()

    # ── Session history ───────────────────────────────────────────────────────
    history = st.session_state.history
    if len(history) > 1:
        st.markdown("---")
        st.markdown("""
        <div style="font-family:'Nunito',sans-serif;font-weight:800;
                    color:#1E293B;font-size:0.85rem;margin-bottom:8px;">
            Previous questions this session
        </div>
        """, unsafe_allow_html=True)
        for hi, entry in enumerate(history[1:6]):
            pgs    = sorted({r["page"] for r in entry["results"]}) if entry["results"] else []
            pg_str = f"Pages: {', '.join(str(p) for p in pgs)}" if pgs else "No results"
            if st.button(
                f"{entry['question']}  ·  {pg_str}",
                key=f"hist_{hi}_{entry['question'][:15]}",
                use_container_width=True,
            ):
                st.session_state.active_q       = entry["question"]
                st.session_state.active_cat     = entry.get("category", "")
                st.session_state.search_results = entry["results"]
                st.rerun()
