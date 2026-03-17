"""
Page: All Timelines
Every deadline in the SOPM on one page. No scrolling through 124 pages.
"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="All Timelines · IEP Guide", page_icon="⏱️", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("⏱️", "All IEP Timelines", "Every deadline from the SOPM in one place — no more hunting through 124 pages", "#D97706")
status_banner()

TIMELINES = [
    {
        "group": "Initial Evaluation",
        "color": "#2563EB",
        "items": [
            ("60 school days", "Complete all evaluations AND hold IEP meeting", "From date parent signs consent form", "Critical"),
            ("5 school days",  "Send Prior Written Notice of Referral to parent", "From date referral is received", "Critical"),
            ("10 school days", "Schedule Social History meeting with parent", "From date referral is received", "Required"),
            ("Next business day", "Fax referral document into SESIS system", "After receiving referral by hand, mail or fax", "Required"),
        ]
    },
    {
        "group": "Translations & Language",
        "color": "#0D9488",
        "items": [
            ("30 calendar days", "Provide translated IEP or evaluation report to parent", "From date of parent request for translation", "Required"),
            ("Same day as English", "Provide translated notices of meetings and consent forms", "For the 9 DOE covered languages", "Required"),
        ]
    },
    {
        "group": "Annual Review",
        "color": "#7C3AED",
        "items": [
            ("At least once per year", "Review and update the IEP", "Must happen on or before the IEP anniversary date", "Critical"),
            ("April 15 deadline", "Hold IEP meeting if Extended School Year (ESY) is being considered", "Must be completed by April 15 each year", "Required"),
            ("Reasonable notice", "Send written meeting notice to parent", "Must give parent enough time to attend — typically 5+ school days", "Required"),
        ]
    },
    {
        "group": "Reevaluation",
        "color": "#DC2626",
        "items": [
            ("Every 3 years", "Conduct a full reevaluation", "Unless parent and school agree it is unnecessary", "Critical"),
            ("60 school days", "Complete reevaluation when new testing is needed", "From date parent signs consent for reevaluation", "Critical"),
        ]
    },
    {
        "group": "Prior Written Notice",
        "color": "#D97706",
        "items": [
            ("Before any action", "Send Prior Written Notice to parent", "Before proposing or refusing any change to evaluation, IEP or placement", "Critical"),
            ("Same time as PWN", "Provide Procedural Safeguards Notice", "When PWN is required for initial referral or at parent request", "Required"),
            ("At least once per year", "Provide Procedural Safeguards Notice", "At minimum once every 12 months", "Required"),
        ]
    },
    {
        "group": "Surrogate Parent",
        "color": "#16A34A",
        "items": [
            ("10 business days", "Assign a surrogate parent", "When no parent can be identified or located", "Required"),
        ]
    },
    {
        "group": "Discipline",
        "color": "#9333EA",
        "items": [
            ("10 school days", "Hold a Manifestation Determination Review (MDR)", "Before removing a student with an IEP for more than 10 cumulative days", "Critical"),
            ("10 school days", "Maximum suspension without MDR", "After 10 days, special rules apply and MDR may be required", "Critical"),
            ("10 school days", "Provide services during suspension", "School must continue providing educational services", "Required"),
        ]
    },
    {
        "group": "Due Process & Complaints",
        "color": "#E65100",
        "items": [
            ("2 years", "File a due process complaint", "From the date you knew or should have known about the issue", "Important"),
            ("60 calendar days", "State investigates a state complaint", "From date complaint is filed with state education department", "Required"),
            ("30 calendar days", "Resolution period for due process", "School and parent attempt to resolve before hearing", "Required"),
            ("45 days", "Impartial hearing decision issued", "After resolution period ends — can be extended by both parties", "Required"),
        ]
    },
    {
        "group": "Records",
        "color": "#0891B2",
        "items": [
            ("45 days", "School must provide copies of records", "From date parent makes written request for school records", "Required"),
        ]
    },
]

# ── Filter ────────────────────────────────────────────────────────────────────
priority_filter = st.radio("Show", ["All", "Critical only", "Required only"], horizontal=True)
st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)

priority_colors = {"Critical": ("#FEE2E2", "#C62828"), "Required": ("#EFF6FF", "#1E40AF"), "Important": ("#FFF8E1", "#D97706")}

for group in TIMELINES:
    color = group["color"]
    items = group["items"]
    if priority_filter == "Critical only":
        items = [i for i in items if i[3] == "Critical"]
    elif priority_filter == "Required only":
        items = [i for i in items if i[3] in ("Critical","Required")]
    if not items:
        continue

    st.markdown(f"""
    <div style="font-family:'Nunito',sans-serif;font-weight:900;color:{color};
                font-size:0.95rem;text-transform:uppercase;letter-spacing:.05em;
                margin:20px 0 10px;padding-bottom:6px;
                border-bottom:2px solid {color}40;">{group['group']}</div>
    """, unsafe_allow_html=True)

    for deadline, what, when, priority in items:
        pbg, pfg = priority_colors.get(priority, ("#F1F5F9","#475569"))
        st.markdown(f"""
        <div style="display:flex;gap:0;margin-bottom:8px;border-radius:10px;
                    overflow:hidden;border:1px solid #E2E8F0;">
            <div style="background:{color};min-width:130px;padding:14px 16px;
                        display:flex;align-items:center;justify-content:center;text-align:center;">
                <div style="font-family:'Nunito',sans-serif;font-weight:900;
                            color:white;font-size:0.88rem;line-height:1.3;">{deadline}</div>
            </div>
            <div style="background:white;padding:12px 16px;flex:1;">
                <div style="font-weight:700;color:#1E293B;font-size:0.9rem;margin-bottom:3px;">
                    {what}</div>
                <div style="color:#64748B;font-size:0.82rem;">{when}</div>
            </div>
            <div style="background:{pbg};padding:12px 14px;display:flex;
                        align-items:center;min-width:80px;justify-content:center;">
                <span style="color:{pfg};font-size:0.72rem;font-weight:700;
                             text-align:center;">{priority}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Find in PDF
    if st.session_state.get("pdf_loaded"):
        with st.expander(f"What your document says about {group['group']} timelines"):
            results = search_chunks([], group["group"] + " timeline days", top_k=2)
            for r in results:
                st.markdown(f"""
                <div style="background:#F8FAFF;border-left:3px solid {color};
                            border-radius:6px;padding:10px 14px;font-size:0.85rem;
                            line-height:1.8;color:#334155;margin-bottom:6px;">
                    <b>Page {r['page']} · {r['section']}</b><br>{r['text'][:350]}…
                </div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("All timelines based on IDEA federal law and NYC DOE SOPM. Calendar days vs school days differ — school days exclude weekends, holidays and school breaks.")

# Export
if st.button("Download All Timelines as Text"):
    lines = ["IEP TIMELINES REFERENCE\n" + "="*40 + "\n"]
    for g in TIMELINES:
        lines.append(f"\n{g['group'].upper()}\n")
        for d,w,wh,p in g["items"]:
            lines.append(f"  [{d}] {w}\n  When: {wh}\n  Priority: {p}\n")
    st.download_button("Save", "\n".join(lines), "IEP_Timelines.txt", "text/plain")
