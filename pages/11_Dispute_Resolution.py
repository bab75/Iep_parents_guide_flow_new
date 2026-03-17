"""
Page: Dispute Resolution
All 4 options side by side — mediation, state complaint, due process, impartial hearing.
SOPM pages 117-121.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Dispute Resolution · IEP Guide", page_icon="⚖️", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("⚖️", "Dispute Resolution", "If you disagree with the school — you have options. Here is every path explained simply, side by side", "#E65100")
status_banner()

st.info("You never have to accept an IEP you disagree with. Federal law gives you multiple ways to challenge decisions — at no cost to you. These options do not cancel each other out — you can use more than one.")

OPTIONS = [
    {
        "name": "Mediation",
        "icon": "🤝",
        "color": "#16A34A",
        "cost": "Free",
        "time": "30–60 days",
        "formality": "Low",
        "best_for": "When you and the school disagree but both want to work it out. Good first step.",
        "what": "A trained, neutral mediator meets with you and the school to help both sides reach a voluntary agreement. The mediator does not decide — they help you talk it through.",
        "process": ["You request mediation in writing from the state or CSE", "A neutral mediator is assigned — not from your school district", "A meeting is scheduled within a reasonable time", "Both sides explain their position", "If agreement is reached, it is written and legally binding", "If no agreement, you still have all other rights"],
        "pros": ["Free of charge", "Informal and conversational", "Faster than a hearing", "Preserves the relationship with the school", "Agreement is legally binding"],
        "cons": ["Voluntary — school must agree to participate", "No formal decision if no agreement", "Does not stop the clock on other timelines"],
        "sopm": "Pages 117–118",
    },
    {
        "name": "State Complaint",
        "icon": "📬",
        "color": "#2563EB",
        "cost": "Free",
        "time": "60 days for investigation",
        "formality": "Medium",
        "best_for": "When the school violated a specific IDEA requirement. Good for clear violations like missing timelines or failing to provide a service.",
        "what": "You file a written complaint with the state education department (NYSED). The state investigates and issues a written decision. If a violation is found, the state orders corrective action.",
        "process": ["Write a complaint letter describing the specific violation", "Send it to NYSED Office of Special Education", "State has 60 days to investigate and issue a decision", "If violation found, state orders corrective action and compensatory services", "School must implement corrective action within set timeline"],
        "pros": ["Free of charge", "No lawyer needed", "State investigates on your behalf", "Can result in compensatory services", "Addresses systemic violations affecting other families too"],
        "cons": ["Cannot get money damages", "Only addresses violations of IDEA — not disagreements about appropriateness", "State decision may not go in your favor"],
        "sopm": "Pages 117, 120",
    },
    {
        "name": "Due Process Hearing",
        "icon": "🏛️",
        "color": "#D97706",
        "cost": "Free to file — but attorney fees possible",
        "time": "45 days after resolution period",
        "formality": "High — like a court hearing",
        "best_for": "Serious disputes about eligibility, IEP content, placement, or failure to provide FAPE. When other options have failed or the issue is significant.",
        "what": "A formal hearing before an impartial hearing officer (IHO) — like a judge. Both sides present evidence and witnesses. The IHO issues a binding legal decision.",
        "process": ["File a due process complaint in writing with the CSE and state", "School has 15 days to respond", "Resolution meeting within 30 days — both sides try to resolve", "If unresolved, hearing is scheduled within 45 days", "Both sides present evidence and testimony", "IHO issues written decision — legally binding on both parties", "Either party can appeal to State Review Office"],
        "pros": ["Binding legal decision", "Can result in compensatory education and reimbursement", "IHO is independent of the school district", "Can address any IDEA violation or disagreement"],
        "cons": ["Complex and stressful process", "Having an attorney strongly recommended", "Time-consuming — can take months", "School also has legal representation", "Outcome is uncertain"],
        "sopm": "Pages 117–121",
    },
    {
        "name": "Impartial Hearing (IHO Appeal)",
        "icon": "📜",
        "color": "#7C3AED",
        "cost": "Free to file — attorney fees possible",
        "time": "30 days to appeal IHO decision",
        "formality": "Very High",
        "best_for": "When you disagree with the IHO's decision from a due process hearing and want to appeal it.",
        "what": "An appeal of the Impartial Hearing Officer's decision to the State Review Officer (SRO). The SRO reviews the record and can uphold, reverse, or modify the IHO decision.",
        "process": ["File an appeal with the State Review Officer within 30 days of IHO decision", "SRO reviews the hearing record — no new evidence typically", "SRO issues a written decision", "Either party can then appeal to state or federal court"],
        "pros": ["Independent second review", "Can correct IHO errors", "Part of the formal appeals process"],
        "cons": ["Same complexity as the original hearing", "Attorney almost always needed", "Time-consuming", "Outcome is uncertain"],
        "sopm": "Pages 120–121",
    },
]

# ── Side-by-side comparison ───────────────────────────────────────────────────
st.markdown("### Quick Comparison")
cols = st.columns(4)
for col, opt in zip(cols, OPTIONS):
    with col:
        st.markdown(f"""
        <div style="background:{opt['color']};border-radius:12px;padding:16px;
                    text-align:center;margin-bottom:12px;">
            <div style="font-size:1.8rem;margin-bottom:6px;">{opt['icon']}</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:900;
                        color:white;font-size:0.95rem;">{opt['name']}</div>
        </div>
        <div style="font-size:0.82rem;color:#374151;margin-bottom:5px;">
            <b>Cost:</b> {opt['cost']}</div>
        <div style="font-size:0.82rem;color:#374151;margin-bottom:5px;">
            <b>Time:</b> {opt['time']}</div>
        <div style="font-size:0.82rem;color:#374151;margin-bottom:10px;">
            <b>Formality:</b> {opt['formality']}</div>
        <div style="background:{opt['color']}12;border-radius:7px;padding:8px;
                    font-size:0.8rem;color:#334155;line-height:1.5;">
            <b>Best for:</b><br>{opt['best_for']}</div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Full Details — Click Each Option")

for opt in OPTIONS:
    color = opt["color"]
    with st.expander(f"{opt['icon']}  {opt['name']}  ·  {opt['cost']}  ·  {opt['time']}"):
        d1, d2 = st.columns(2)
        with d1:
            st.markdown(f"""
            <div style="background:{color}0D;border-left:4px solid {color};
                        border-radius:8px;padding:14px;margin-bottom:10px;">
                <div style="font-weight:700;color:{color};font-size:0.82rem;
                            margin-bottom:6px;">WHAT IT IS</div>
                <div style="color:#334155;font-size:0.87rem;line-height:1.75;">{opt['what']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**Step-by-step process:**")
            for i, step in enumerate(opt["process"], 1):
                st.markdown(f"""
                <div style="display:flex;gap:8px;padding:5px 0;font-size:0.84rem;color:#374151;">
                    <span style="background:{color};color:white;border-radius:50%;
                                 min-width:20px;height:20px;display:flex;align-items:center;
                                 justify-content:center;font-size:0.7rem;font-weight:700;
                                 flex-shrink:0;">{i}</span>
                    <span>{step}</span>
                </div>
                """, unsafe_allow_html=True)

        with d2:
            pros_html = "".join(f'<div style="color:#166534;font-size:0.84rem;padding:3px 0;">✓ {p}</div>' for p in opt["pros"])
            cons_html = "".join(f'<div style="color:#C62828;font-size:0.84rem;padding:3px 0;">✗ {c}</div>' for c in opt["cons"])
            st.markdown(f"""
            <div style="background:#F0FDF4;border-radius:8px;padding:12px;margin-bottom:8px;">
                <div style="font-weight:700;color:#15803D;font-size:0.78rem;
                            margin-bottom:6px;">ADVANTAGES</div>{pros_html}
            </div>
            <div style="background:#FEF2F2;border-radius:8px;padding:12px;margin-bottom:8px;">
                <div style="font-weight:700;color:#DC2626;font-size:0.78rem;
                            margin-bottom:6px;">DISADVANTAGES</div>{cons_html}
            </div>
            <div style="background:#EFF6FF;border-radius:8px;padding:10px;">
                <div style="font-size:0.78rem;color:#1E40AF;font-weight:700;">
                    SOPM Reference: {opt['sopm']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("pdf_loaded"):
            results = search_chunks([], opt["name"] + " complaint hearing", top_k=1)
            if results:
                r = results[0]
                st.markdown(f"""
                <div style="background:#F8FAFF;border-left:3px solid {color};
                            border-radius:6px;padding:10px 14px;margin-top:8px;
                            font-size:0.83rem;color:#334155;line-height:1.75;">
                    <b>📄 From your document — Page {r['page']}:</b><br>{r['text'][:350]}…
                </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="background:#FFF8E1;border-radius:10px;padding:16px;font-size:0.87rem;color:#92400E;">
    <b>Important:</b> During any dispute, the Stay Put rule applies — your child has the right to remain
    in their current placement and continue receiving current services while the dispute is resolved.
    The school cannot move your child during an active complaint or hearing without your consent.
</div>
""", unsafe_allow_html=True)
