"""
Page: Glossary
Every IEP term explained in plain English. Terms detected from the uploaded PDF.
"""
import streamlit as st, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Glossary · IEP Guide", page_icon="📖", layout="wide")

from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

page_header("📖", "Glossary",
            "Every IEP term explained in plain language — no more confusing abbreviations",
            "#16A34A")
status_banner()

# ── Master glossary (federal IDEA terms — always available) ───────────────────
GLOSSARY = [
    ("IDEA", "Individuals with Disabilities Education Act",
     "The federal law that guarantees special education services for children with disabilities. Every school in the US must follow IDEA.",
     "General"),
    ("IEP", "Individualized Education Program",
     "A written document that describes your child's disability, current abilities, annual goals, what services they will receive, where they will be educated, and any accommodations. It is legally binding.",
     "Core Documents"),
    ("CSE", "Committee on Special Education",
     "The official team that makes IEP decisions in New York. Called different names in different states (IEP Team, ARD Committee, etc.). You are a required member.",
     "People & Teams"),
    ("FAPE", "Free Appropriate Public Education",
     "What IDEA guarantees every eligible student. 'Free' means no cost to the family. 'Appropriate' means designed to meet the child's unique needs. Not the best possible education — but an appropriate one.",
     "Core Concepts"),
    ("LRE", "Least Restrictive Environment",
     "The legal requirement that students with disabilities be educated alongside non-disabled students as much as possible. Moving to a more restrictive setting requires written justification.",
     "Core Concepts"),
    ("PWN", "Prior Written Notice",
     "A written document the school must give you BEFORE making any change to your child's evaluation, placement, or services. It must explain what they are proposing or refusing, and why.",
     "Documents"),
    ("IEE", "Independent Educational Evaluation",
     "An evaluation done by someone outside the school district, at the school's expense, when you disagree with the school's evaluation. You have the right to request this.",
     "Evaluations"),
    ("Present Levels", "Present Levels of Academic Achievement and Functional Performance",
     "The section of the IEP that describes how your child is doing right now — academically and in daily functioning. Every goal in the IEP must connect to something described in Present Levels.",
     "IEP Sections"),
    ("Annual Goals", "Measurable Annual Goals",
     "Specific, measurable targets your child should reach within one year. A good goal has: a starting point, a target, a method of measurement, and a timeline. 'Will improve reading' is not a measurable goal.",
     "IEP Sections"),
    ("ESY", "Extended School Year",
     "Special education services provided during summer break (or other school breaks) for students who would significantly lose skills without year-round support.",
     "Services"),
    ("BIP", "Behavioral Intervention Plan",
     "A written plan that describes strategies to help a student with challenging behaviors. Must be based on a Functional Behavioral Assessment (FBA). Uses positive strategies — not punishment.",
     "Documents"),
    ("FBA", "Functional Behavioral Assessment",
     "An evaluation that examines WHY a student behaves a certain way in school. Must be done before a BIP is written. Looks at what triggers the behavior and what the student gets from it.",
     "Evaluations"),
    ("OT", "Occupational Therapy",
     "A related service that helps students with fine motor skills, handwriting, sensory processing, and daily living activities. Provided by a licensed occupational therapist.",
     "Related Services"),
    ("PT", "Physical Therapy",
     "A related service for students with physical disabilities affecting their ability to move, balance, or participate in school. Provided by a licensed physical therapist.",
     "Related Services"),
    ("SLP / Speech", "Speech-Language Pathology",
     "A related service for students with communication needs — including articulation (how words sound), language (understanding and using words), fluency (stuttering), and voice.",
     "Related Services"),
    ("ICT", "Integrated Co-Teaching",
     "A classroom where a general education teacher and a special education teacher co-teach together. Up to 40% of students can have IEPs. The student remains in the general education setting.",
     "Placements"),
    ("Resource Room", "Resource Room",
     "A placement where a student leaves the general education classroom for part of the day to receive specialized instruction in a small group from a special education teacher.",
     "Placements"),
    ("12:1:1", "Special Class Ratio 12:1:1",
     "A special education class with 12 students, 1 teacher, and 1 paraprofessional. All students have IEPs. The curriculum is specialized. Used when a student needs intensive support for most of the school day.",
     "Placements"),
    ("Paraprofessional / Para", "Paraprofessional or Teaching Assistant",
     "A school staff member who provides direct support to a student with a disability. Can be assigned to an individual student (1:1 para) or shared among a group.",
     "People & Teams"),
    ("Surrogate Parent", "Surrogate Parent",
     "An adult appointed by the school district to act as a parent when the biological or foster parent cannot be located or is unavailable to participate in IEP decisions.",
     "People & Teams"),
    ("Transition Plan", "Transition Services Plan",
     "Required in the IEP for students age 15 (and sometimes 14). Describes goals for life after high school — college, employment, independent living — and what services will help reach those goals.",
     "IEP Sections"),
    ("Stay Put / Pendency", "Stay Put / Pendency",
     "The legal rule that while any dispute is being resolved, your child has the right to remain in their current placement and continue receiving their current services. The school cannot move your child during a disagreement.",
     "Legal Rights"),
    ("Due Process", "Due Process Hearing",
     "A formal legal proceeding before an impartial hearing officer to resolve a dispute between parents and the school about a child's IEP, evaluation, or placement. Both sides can present evidence.",
     "Legal Rights"),
    ("Mediation", "Mediation",
     "A free, voluntary process where a neutral trained mediator helps parents and the school reach an agreement. Faster and less formal than a due process hearing. Does not give up other rights.",
     "Legal Rights"),
    ("Section 504", "Section 504 of the Rehabilitation Act",
     "A different law from IDEA that prohibits disability discrimination in schools. Students who do not qualify for an IEP under IDEA may still qualify for a 504 Plan with accommodations.",
     "Related Laws"),
    ("MDR", "Manifestation Determination Review",
     "A meeting required before a school can suspend or expel a student with a disability for more than 10 days. The team must determine whether the behavior was caused by the disability.",
     "Discipline"),
    ("RTI / MTSS", "Response to Intervention / Multi-Tiered System of Supports",
     "A framework of increasing levels of support for ALL students before or alongside special education referral. RTI data can be used as part of an evaluation but cannot be used to delay or deny one.",
     "General"),
    ("SESIS", "Special Education Student Information System",
     "NYC's computer system for managing IEP documents. Only relevant for NYC schools — other districts use different systems.",
     "Systems"),
    ("Prior Written Notice", "Prior Written Notice (PWN)",
     "Same as PWN above. The school must give you this in writing before changing, proposing, or refusing anything about your child's IEP.",
     "Documents"),
]

# ── Controls ──────────────────────────────────────────────────────────────────
all_cats = sorted(set(t[3] for t in GLOSSARY))
c1, c2 = st.columns([2, 1])
with c1:
    search = st.text_input("Search terms", placeholder="Type a term or abbreviation…",
                            label_visibility="collapsed")
with c2:
    cat_filter = st.selectbox("Category", ["All"] + all_cats, label_visibility="collapsed")

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = GLOSSARY
if search:
    sf = search.lower()
    filtered = [t for t in filtered if sf in t[0].lower() or sf in t[1].lower() or sf in t[2].lower()]
if cat_filter != "All":
    filtered = [t for t in filtered if t[3] == cat_filter]

st.markdown(f"""
<div style="color:#64748B;font-size:0.82rem;margin-bottom:16px;">
    Showing {len(filtered)} of {len(GLOSSARY)} terms
</div>
""", unsafe_allow_html=True)

# ── Render by category ────────────────────────────────────────────────────────
cat_color = {
    "Core Concepts":"#DC2626","Core Documents":"#7C3AED","Documents":"#7C3AED",
    "IEP Sections":"#2563EB","People & Teams":"#0D9488","Evaluations":"#7C3AED",
    "Services":"#D97706","Related Services":"#D97706","Placements":"#16A34A",
    "Legal Rights":"#DC2626","Related Laws":"#B45309","Discipline":"#9333EA",
    "Systems":"#475569","General":"#475569",
}

display_cats = sorted(set(t[3] for t in filtered))
for cat in display_cats:
    cat_terms = [t for t in filtered if t[3] == cat]
    if not cat_terms:
        continue
    color = cat_color.get(cat, "#475569")

    st.markdown(f"""
    <div style="font-family:'Nunito',sans-serif;font-weight:900;color:{color};
                font-size:0.9rem;text-transform:uppercase;letter-spacing:0.06em;
                margin:20px 0 10px;padding-bottom:6px;
                border-bottom:2px solid {color}30;">{cat}</div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, (abbr, full, defn, _) in enumerate(cat_terms):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:white;border:1px solid #E2E8F0;
                        border-left:4px solid {color};border-radius:10px;
                        padding:14px 16px;margin-bottom:10px;">
                <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:6px;
                            flex-wrap:wrap;">
                    <span style="font-family:'Nunito',sans-serif;font-weight:900;
                                 color:{color};font-size:1rem;">{abbr}</span>
                    <span style="color:#64748B;font-size:0.8rem;font-style:italic;">
                        {full}</span>
                </div>
                <div style="color:#374151;font-size:0.87rem;line-height:1.75;">
                    {defn}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.pdf_loaded:
                if st.button(f"Find '{abbr}' in my document",
                              key=f"gl_{abbr[:10]}_{i}", use_container_width=True):
                    results = search_chunks(
                        [], f"{abbr} {full}", top_k=1
                    )
                    st.session_state[f"gl_result_{abbr}"] = results

                cached = st.session_state.get(f"gl_result_{abbr}", [])
                if cached:
                    r = cached[0]
                    st.markdown(f"""
                    <div style="background:#EFF6FF;border-radius:6px;padding:8px 12px;
                                font-size:0.8rem;color:#1E40AF;line-height:1.65;
                                margin-bottom:8px;">
                        📄 Page {r['page']}: {r['text'][:200]}…</div>
                    """, unsafe_allow_html=True)
