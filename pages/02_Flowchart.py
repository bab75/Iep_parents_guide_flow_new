"""
Page: Process Flowchart
Visual map of the IEP journey. Each step shows what the document says.
"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Flowchart · IEP Guide", page_icon="🗺️", layout="wide")

from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner, answer_card

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

page_header("🗺️", "IEP Process Flowchart",
            "The complete IEP journey from start to finish — click any step to see what your document says",
            "#0D9488")
status_banner()

# ── Process steps with search queries matched to SOP content ──────────────────
STEPS = [
    {
        "id": 1, "phase": "Start",
        "title": "You suspect your child needs help",
        "plain": "You notice your child is struggling in school — with learning, behavior, speech, or other areas. You have the right to ask for an evaluation at any time.",
        "query": "referral child find disability suspected",
        "color": "#2563EB", "icon": "🏠",
        "questions": ["Does the school have to find children who need help?",
                      "Can I request an evaluation myself?"],
    },
    {
        "id": 2, "phase": "Referral",
        "title": "You submit a written referral",
        "plain": "Write a letter to the school or CSE office asking for a special education evaluation. Keep a copy. The date you submit this starts the process.",
        "query": "referral written request initial process",
        "color": "#2563EB", "icon": "✉️",
        "questions": ["How do I make a referral?", "What should be in my referral letter?"],
    },
    {
        "id": 3, "phase": "Notification",
        "title": "School contacts you within 10 school days",
        "plain": "The school must reach out to you quickly. A social worker will explain your rights and schedule a Social History Interview.",
        "query": "notification parent contact social history interview",
        "color": "#0D9488", "icon": "📞",
        "questions": ["How soon must the school respond?", "What is a Social History Interview?"],
    },
    {
        "id": 4, "phase": "Consent",
        "title": "You sign consent to evaluate",
        "plain": "Before any testing begins, you must give written permission. The 60-day clock starts the moment you sign. You can consent to some tests and not others.",
        "query": "parental consent evaluation written sign",
        "color": "#0D9488", "icon": "✍️",
        "questions": ["What am I consenting to?", "What if I only agree to some tests?"],
    },
    {
        "id": 5, "phase": "Evaluation",
        "title": "Team evaluates your child (within 60 days)",
        "plain": "A team of specialists evaluates every area of suspected disability. They cannot rely on just one test. You can provide your own information to the team.",
        "query": "evaluation assessment 60 day multiple tools specialists",
        "color": "#7C3AED", "icon": "🔬",
        "questions": ["Who conducts the evaluation?", "What tests will be used?",
                      "What if I disagree with the results?"],
    },
    {
        "id": 6, "phase": "Eligibility",
        "title": "Team decides if your child is eligible",
        "plain": "Everyone meets to review the evaluation results. You are part of this team. The group decides if your child qualifies under one of the disability categories.",
        "query": "eligibility determination disability category team meeting",
        "color": "#7C3AED", "icon": "⚖️",
        "questions": ["What are the disability categories?", "What if I disagree with eligibility decision?"],
    },
    {
        "id": 7, "phase": "IEP Development",
        "title": "The IEP is written — you are on the team",
        "plain": "If eligible, the team writes the IEP together with you. It includes your child's goals, what services they get, where they will be taught, and what accommodations they receive.",
        "query": "IEP development goals services placement accommodations",
        "color": "#DC2626", "icon": "📝",
        "questions": ["What goes in the IEP?", "What are annual goals?",
                      "What services can be in the IEP?"],
    },
    {
        "id": 8, "phase": "Placement",
        "title": "Placement is decided — must be least restrictive",
        "plain": "The team decides where your child will be educated. By law, they must be with non-disabled students as much as possible. You must be told in writing why the placement was chosen.",
        "query": "placement least restrictive environment LRE special class general education",
        "color": "#DC2626", "icon": "🏫",
        "questions": ["What is Least Restrictive Environment?", "What placement options are there?",
                      "Can I disagree with the placement?"],
    },
    {
        "id": 9, "phase": "Services Begin",
        "title": "Services start — you receive the IEP",
        "plain": "You receive a copy of the complete IEP and a written notice of the placement. Services must begin as soon as possible. All teachers and service providers must follow the IEP.",
        "query": "services begin implementation prior written notice copy IEP",
        "color": "#16A34A", "icon": "🚀",
        "questions": ["When do services start?", "What is Prior Written Notice?",
                      "Who must follow the IEP?"],
    },
    {
        "id": 10, "phase": "Annual Review",
        "title": "IEP reviewed every year",
        "plain": "At least once a year, the team meets to review your child's progress, update goals, and revise the IEP. You are always invited and your input matters.",
        "query": "annual review IEP meeting yearly progress goals",
        "color": "#16A34A", "icon": "📅",
        "questions": ["What happens at the annual review?", "When must the review happen?"],
    },
    {
        "id": 11, "phase": "Reevaluation",
        "title": "Full reevaluation every 3 years",
        "plain": "Every 3 years (or when requested), the team does a full reevaluation to check if your child still qualifies and if their needs have changed.",
        "query": "reevaluation triennial 3 years continued eligibility",
        "color": "#D97706", "icon": "🔄",
        "questions": ["What is a reevaluation?", "Can I request a reevaluation sooner?"],
    },
]

# ── Active step state ─────────────────────────────────────────────────────────
if "flow_step" not in st.session_state:
    st.session_state.flow_step = None

# ── Flowchart visual ──────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Nunito',sans-serif;font-weight:800;color:#1E293B;
            font-size:1rem;margin-bottom:12px;">
    Click any step to see what your document says about it
</div>
""", unsafe_allow_html=True)

# Render steps in a responsive grid
cols_per_row = 4
rows = [STEPS[i:i+cols_per_row] for i in range(0, len(STEPS), cols_per_row)]

for row_steps in rows:
    cols = st.columns(len(row_steps))
    for col, step in zip(cols, row_steps):
        with col:
            is_active = st.session_state.flow_step == step["id"]
            border    = f"3px solid {step['color']}" if is_active else "2px solid #E2E8F0"
            bg        = f"{step['color']}12" if is_active else "white"
            btn_label = f"{'▶ ' if is_active else ''}{step['icon']} Step {step['id']}\n{step['title']}"
            if st.button(btn_label, key=f"flow_{step['id']}", use_container_width=True):
                if st.session_state.flow_step == step["id"]:
                    st.session_state.flow_step = None
                else:
                    st.session_state.flow_step = step["id"]
                st.rerun()

            # Phase badge
            st.markdown(f"""
            <div style="text-align:center;margin-top:-6px;margin-bottom:4px;">
                <span style="background:{step['color']}18;color:{step['color']};
                             border-radius:8px;padding:1px 8px;font-size:0.7rem;
                             font-weight:700;">{step['phase']}</span>
            </div>
            """, unsafe_allow_html=True)

    # Connector arrow between rows (except after last row)
    if row_steps != rows[-1]:
        st.markdown("""
        <div style="text-align:center;color:#94A3B8;font-size:1.4rem;margin:2px 0;">↓</div>
        """, unsafe_allow_html=True)

# ── Detail panel for active step ──────────────────────────────────────────────
if st.session_state.flow_step:
    step = next(s for s in STEPS if s["id"] == st.session_state.flow_step)
    st.markdown("---")

    h1, h2 = st.columns([1, 2], gap="large")

    with h1:
        st.markdown(f"""
        <div style="background:{step['color']}10;border:2px solid {step['color']}40;
                    border-radius:14px;padding:20px;">
            <div style="font-size:2.5rem;margin-bottom:10px;">{step['icon']}</div>
            <div style="font-size:0.72rem;font-weight:700;color:{step['color']};
                        text-transform:uppercase;letter-spacing:0.06em;
                        margin-bottom:4px;">Step {step['id']} · {step['phase']}</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:800;
                        color:#1E293B;font-size:1.05rem;margin-bottom:12px;">
                {step['title']}</div>
            <div style="color:#475569;font-size:0.9rem;line-height:1.75;
                        background:white;border-radius:10px;padding:14px;">
                {step['plain']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Questions for this step
        st.markdown("""
        <div style="font-family:'Nunito',sans-serif;font-weight:800;
                    color:#1E293B;font-size:0.88rem;margin:14px 0 8px;">
            Common questions at this step:
        </div>
        """, unsafe_allow_html=True)
        for q in step["questions"]:
            if st.button(q, key=f"stepq_{q[:20]}", use_container_width=True):
                if st.session_state.pdf_loaded:
                    results = search_chunks([], q, top_k=3)
                    st.session_state.step_results     = results
                    st.session_state.step_active_q    = q
                else:
                    st.warning("Upload a PDF first.")

    with h2:
        st.markdown(f"""
        <div style="font-family:'Nunito',sans-serif;font-weight:800;
                    color:#1E293B;font-size:0.95rem;margin-bottom:10px;">
            What your document says about: <em>{step['title']}</em>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.pdf_loaded:
            # Auto-search for this step's content
            if f"step_results_{step['id']}" not in st.session_state:
                results = search_chunks(
                    [], step["query"], top_k=3
                )
                st.session_state[f"step_results_{step['id']}"] = results

            results = st.session_state.get(f"step_results_{step['id']}", [])

            # Override with question search if active
            if st.session_state.get("step_active_q"):
                results  = st.session_state.get("step_results", results)
                query_lbl = st.session_state.step_active_q
            else:
                query_lbl = step["title"]

            if results:
                for i, r in enumerate(results, 1):
                    answer_card(r, query_lbl, i)
            else:
                st.info("Upload your PDF on the Home page to see what your document says about this step.")

            # Clear step question after displaying
            if "step_active_q" in st.session_state:
                del st.session_state["step_active_q"]
                if "step_results" in st.session_state:
                    del st.session_state["step_results"]
        else:
            st.info("Upload your PDF on the Home page to see your document's content for each step.")
