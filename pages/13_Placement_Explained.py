"""
Page: Placement Explainer
Visual LRE continuum — all placement types from SOPM pages 69-80.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Placement Explained · IEP Guide", page_icon="🏫", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("🏫", "Placement Explained", "Every placement type in the SOPM — what it means, what to expect, and what to ask", "#2563EB")
status_banner()

st.info("**Placement** means WHERE and HOW your child is educated. Federal law requires the **Least Restrictive Environment (LRE)** — your child must be educated with non-disabled students as much as possible. More restrictive placements require written justification.")

PLACEMENTS = [
    {"level":1,"name":"General Education with Accommodations (504 Plan)","abbr":"504",
     "color":"#16A34A","restrict":"Least Restrictive",
     "what":"Your child stays in a regular classroom full time. They receive accommodations — changes in HOW they learn — but do not receive specialized instruction from a special education teacher. This is NOT an IEP.",
     "looks_like":"Extended time on tests, read-aloud, preferential seating, reduced assignment length, use of calculator.",
     "right_for":"When the disability affects school but specialized instruction is not needed — only accommodations.",
     "ask":"If the team recommends only a 504, ask: Does my child need specialized instruction, not just accommodations? Could they benefit from an IEP instead?",
     "sopm":"Pages 69, 71"},
    {"level":2,"name":"Consultant Teacher (CT)","abbr":"CT",
     "color":"#0D9488","restrict":"Very Low Restriction",
     "what":"A special education teacher consults with and supports your child's general education teacher. The special ed teacher may come into the classroom but primarily works behind the scenes advising the general ed teacher on how to support your child.",
     "looks_like":"The general ed teacher adjusts materials, modifies instructions, and uses strategies recommended by the special ed consultant.",
     "right_for":"Students who can access the general education curriculum with indirect support.",
     "ask":"How often does the consultant come into the classroom? What specific changes are being made to support my child?",
     "sopm":"Pages 69, 72"},
    {"level":3,"name":"Resource Room","abbr":"RR",
     "color":"#2563EB","restrict":"Low Restriction",
     "what":"Your child leaves the general education classroom for part of the day to receive specialized small-group instruction from a special education teacher. The rest of the day is spent in the general education classroom.",
     "looks_like":"Your child goes to a resource room 3–5 times per week for 40 minutes to work on reading, math, or writing goals in a small group of 5 or fewer students.",
     "right_for":"Students who need direct specialized instruction in specific areas but can access general education for most of the day.",
     "ask":"How many students are in the resource room group? What specific skills are being targeted?",
     "sopm":"Pages 69, 72"},
    {"level":4,"name":"Integrated Co-Teaching (ICT)","abbr":"ICT",
     "color":"#7C3AED","restrict":"Low–Medium Restriction",
     "what":"A general education teacher and a special education teacher co-teach the same class together. Up to 40% of students in the class may have IEPs. Your child remains in the general education setting but with two teachers providing support.",
     "looks_like":"Your child is in a class of 25 students — 10 have IEPs. Both teachers teach together, plan together, and both support all students.",
     "right_for":"Students who benefit from the general education curriculum but need more intensive in-class support.",
     "ask":"What percentage of students in the class have IEPs? How are both teachers sharing responsibility for all students?",
     "sopm":"Pages 69, 72–73, 93–96"},
    {"level":5,"name":"Special Class 12:1:1","abbr":"SC 12:1:1",
     "color":"#D97706","restrict":"Moderate Restriction",
     "what":"A separate classroom with 12 students with disabilities, 1 special education teacher, and 1 paraprofessional. The curriculum is specialized and adapted to IEP goals. Students may leave for specials or lunch with general education peers.",
     "looks_like":"12 students all with IEPs. Adapted materials, modified curriculum, individualized instruction. Smaller class allows more attention per student.",
     "right_for":"Students who need specialized instruction for more than half the school day and whose IEP goals cannot be met in general education settings.",
     "ask":"Will my child have ANY time with non-disabled peers? What is the plan to move toward a less restrictive setting?",
     "sopm":"Pages 72–73, 93–96"},
    {"level":6,"name":"Special Class 8:1:1","abbr":"SC 8:1:1",
     "color":"#E65100","restrict":"High Restriction",
     "what":"A smaller special class with 8 students, 1 teacher, and 1 paraprofessional. Higher staff-to-student ratio for more intensive support.",
     "looks_like":"8 students with significant academic or behavioral needs. More individualized attention. Curriculum is highly adapted.",
     "right_for":"Students with more significant needs who require higher intensity of support.",
     "ask":"What specific needs require this ratio vs the 12:1:1? Is there a plan to move toward 12:1:1 if appropriate?",
     "sopm":"Pages 72–73"},
    {"level":7,"name":"Special Class 6:1:1","abbr":"SC 6:1:1",
     "color":"#DC2626","restrict":"Very High Restriction",
     "what":"The most intensive special class setting — 6 students with significant disabilities, 1 teacher, 1 paraprofessional. For students with substantial behavioral, medical, or educational needs.",
     "looks_like":"Very small class. Highly individualized instruction. May include students with Emotional Disturbance, significant behavioral needs, or complex multiple disabilities.",
     "right_for":"Students whose needs cannot be safely or appropriately addressed in a larger group.",
     "ask":"Why is a 6:1:1 needed rather than 8:1:1? What are the specific behaviors or needs that require this ratio?",
     "sopm":"Page 73"},
    {"level":8,"name":"District 75 — Specialized School","abbr":"D75",
     "color":"#9333EA","restrict":"High–Very High Restriction",
     "what":"NYC's District 75 provides highly specialized programs for students with the most significant disabilities — including Autism, Intellectual Disability, Multiple Disabilities, and Deaf-Blindness. Separate school buildings specifically designed for this population.",
     "looks_like":"Separate school with specialized staff, therapists on-site, sensory rooms, life skills programming, and adapted academic instruction.",
     "right_for":"Students whose needs are so significant that they cannot be met even in a 6:1:1 setting in a general education school.",
     "ask":"What general education contact will my child have? What is the long-term plan? Is there a less restrictive D75 setting?",
     "sopm":"Pages 49, 73"},
    {"level":9,"name":"State-Approved Non-Public School (NPS)","abbr":"NPS",
     "color":"#7F1D1D","restrict":"Very High Restriction",
     "what":"A private school that has been approved by NYSED to serve students with disabilities whose needs cannot be met in public school settings. The DOE pays tuition. The NPS provides specialized programming.",
     "looks_like":"Small school specifically designed for students with complex needs — often focused on specific disabilities like Autism, Emotional Disturbance, or multiple disabilities.",
     "right_for":"Students whose needs cannot be met in any available public school program.",
     "ask":"What specific needs cannot be met in a public school? What NPS programs were considered? Can my child transition back to public school?",
     "sopm":"Pages 70–71, 99"},
    {"level":10,"name":"Home Instruction","abbr":"HI",
     "color":"#374151","restrict":"Most Restrictive",
     "what":"Education provided in the student's home by a DOE-assigned teacher. Temporary, for students who cannot attend school due to medical reasons. This is NOT the same as homeschooling.",
     "looks_like":"A teacher comes to the home several times per week. Instruction is individual, based on the IEP.",
     "right_for":"Students with medical conditions that temporarily prevent school attendance. Should be reviewed within 6 months.",
     "ask":"When will my child return to school? Is all IEP services being provided at home? When will this placement be reviewed?",
     "sopm":"Pages 100, 39"},
]

# ── Visual continuum ──────────────────────────────────────────────────────────
st.markdown("### The LRE Continuum — Least to Most Restrictive")
st.caption("Your child must be placed in the least restrictive environment where they can make meaningful progress with appropriate supports.")

for p in PLACEMENTS:
    bar   = "▓" * p["level"] + "░" * (10 - p["level"])
    color = p["color"]
    with st.expander(f"Level {p['level']} — {p['abbr']}  ·  {p['name']}  ·  {p['restrict']}"):
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <span style="font-family:'Nunito',sans-serif;color:{color};
                         font-size:1.1rem;letter-spacing:2px;">{bar}</span>
            <span style="background:{color}18;color:{color};border-radius:6px;
                         padding:3px 12px;font-size:0.78rem;font-weight:700;">{p['restrict']}</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:{color}0D;border-left:4px solid {color};
                        border-radius:8px;padding:13px;margin-bottom:9px;">
                <div style="font-weight:700;color:{color};font-size:0.78rem;margin-bottom:5px;">WHAT IT IS</div>
                <div style="color:#334155;font-size:0.87rem;line-height:1.75;">{p['what']}</div>
            </div>
            <div style="background:#F8FAFF;border-radius:8px;padding:11px;">
                <div style="font-weight:700;color:#475569;font-size:0.78rem;margin-bottom:4px;">WHAT IT LOOKS LIKE DAY TO DAY</div>
                <div style="color:#334155;font-size:0.85rem;line-height:1.65;">{p['looks_like']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#F0FDF4;border-radius:8px;padding:11px;margin-bottom:9px;">
                <div style="font-weight:700;color:#15803D;font-size:0.78rem;margin-bottom:4px;">RIGHT FOR YOUR CHILD WHEN</div>
                <div style="color:#334155;font-size:0.85rem;line-height:1.65;">{p['right_for']}</div>
            </div>
            <div style="background:#FFF8E1;border-radius:8px;padding:11px;margin-bottom:9px;">
                <div style="font-weight:700;color:#D97706;font-size:0.78rem;margin-bottom:4px;">QUESTIONS TO ASK</div>
                <div style="color:#334155;font-size:0.85rem;font-style:italic;line-height:1.65;">{p['ask']}</div>
            </div>
            <div style="background:#EFF6FF;border-radius:6px;padding:8px;">
                <div style="font-size:0.75rem;color:#1E40AF;font-weight:700;">SOPM: {p['sopm']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("pdf_loaded"):
            results = search_chunks([], p["name"] + " placement", top_k=1)
            if results:
                r = results[0]
                st.markdown(f"""
                <div style="background:#F8FAFF;border-left:3px solid {color};
                            border-radius:6px;padding:9px 12px;margin-top:6px;
                            font-size:0.82rem;color:#334155;line-height:1.7;">
                    <b>📄 Page {r['page']}:</b> {r['text'][:280]}…</div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="background:#FFF1F2;border-radius:10px;padding:14px 18px;font-size:0.87rem;color:#9F1239;">
    <b>Your right:</b> If you disagree with the placement recommendation, ask in writing:
    "What less restrictive option was considered and why was it rejected?"
    The school must document this in the IEP. If you still disagree, you can request mediation
    or file a state complaint. See the Dispute Resolution page.
</div>
""", unsafe_allow_html=True)
