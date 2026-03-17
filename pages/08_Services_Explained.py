"""
Page: Services Explainer
Every service type in the SOPM explained in plain English.
SETSS, ICT, OT, PT, SLP, special class — no jargon.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Services Explained · IEP Guide", page_icon="🧩", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("🧩", "IEP Services Explained", "Every service your child can receive — what it is, where it happens, and what good looks like", "#7C3AED")
status_banner()

SERVICES = {
    "Special Education Instruction": [
        {
            "name": "SETSS — Special Education Teacher Support Services",
            "abbr": "SETSS",
            "what": "A special education teacher works directly with your child in a small group — usually 3 to 5 students — to provide specialized instruction in reading, writing, math, or other areas where they need help.",
            "where": "Usually in a separate room (pull-out) or can be in the general education classroom (push-in). Your IEP specifies which.",
            "how_often": "Specified in the IEP service grid — typically 3 to 5 times per week. Each session is usually 40 minutes.",
            "good_sign": "Your child's teacher communicates regularly, shares progress data, and the goals in the IEP match what is being worked on in sessions.",
            "red_flag": "Your child never leaves for SETSS, sessions are cancelled repeatedly, or you haven't been updated on progress.",
            "ask": "What specific skills is my child working on in SETSS? How do you measure progress? Can I see data?",
            "color": "#2563EB",
        },
        {
            "name": "ICT — Integrated Co-Teaching",
            "abbr": "ICT",
            "what": "A general education teacher and a special education teacher co-teach the same classroom together. Up to 40% of students in the class may have IEPs. Your child stays in the general education room full-time but gets support from both teachers.",
            "where": "In the general education classroom. Your child is never pulled out for ICT.",
            "how_often": "All day — this is a classroom setting, not a session.",
            "good_sign": "Both teachers actively support all students. The class size is appropriate and both teachers are truly co-teaching, not one teaching and one helping.",
            "red_flag": "The special education teacher only works with students with IEPs in the back of the room. The class has too many students. Only one teacher is ever teaching.",
            "ask": "How do the two teachers share responsibility? What percentage of students in the class have IEPs?",
            "color": "#0D9488",
        },
        {
            "name": "CTT — Collaborative Team Teaching",
            "abbr": "CTT",
            "what": "Similar to ICT — two teachers co-teach a class. CTT is an older term that NYC DOE has largely replaced with ICT. You may still see it in older IEPs.",
            "where": "In the general education classroom.",
            "how_often": "Full school day setting.",
            "good_sign": "Both teachers are qualified and actively involved in instruction for all students.",
            "red_flag": "One teacher is clearly in charge and the other is just assisting.",
            "ask": "Is this still being called CTT or has it been updated to ICT in SESIS?",
            "color": "#0891B2",
        },
        {
            "name": "Consultant Teacher",
            "abbr": "CT",
            "what": "A special education teacher consults with the general education teacher about how to support your child. The special ed teacher may come into the classroom to observe or model strategies, but does not directly teach your child in most cases.",
            "where": "In the general education classroom as support, or in planning meetings with teachers.",
            "how_often": "Varies — the IEP specifies the frequency.",
            "good_sign": "Teachers are adapting instruction and materials based on the consultant's recommendations.",
            "red_flag": "You never hear about what the consultant teacher is doing. No changes in how your child is taught.",
            "ask": "What specific strategies is the consultant teacher recommending? How are they being implemented?",
            "color": "#16A34A",
        },
        {
            "name": "Special Class",
            "abbr": "SC",
            "what": "A classroom with only students who have IEPs. Smaller class size with a special education teacher and a paraprofessional. The curriculum is specialized and adapted to each student's IEP goals.",
            "where": "In a separate classroom from general education students. Three common ratios — 12:1:1, 8:1:1, or 6:1:1 (students : teacher : paraprofessional).",
            "how_often": "Full school day or most of the school day.",
            "good_sign": "Your child is making progress on IEP goals. There are opportunities to interact with non-disabled peers during lunch, specials, etc.",
            "red_flag": "No interaction with general education students at all. Goals haven't changed in years. No progress data shared with you.",
            "ask": "What is the class ratio? Are there any opportunities for my child to be with general education students? What is the least restrictive option that was considered?",
            "color": "#DC2626",
        },
    ],
    "Related Services": [
        {
            "name": "Speech-Language Therapy",
            "abbr": "SLP / Speech",
            "what": "A licensed Speech-Language Pathologist works with your child on communication skills. This includes how clearly they speak (articulation), how well they understand and use language, fluency (stuttering), and voice. It can also include AAC — communication devices for students who cannot speak.",
            "where": "Individual or small group sessions, either pull-out or in the classroom.",
            "how_often": "Specified in IEP — commonly 2 to 3 times per week for 30–40 minutes.",
            "good_sign": "The therapist communicates goals clearly, involves you in home practice strategies, and you see progress on measurable goals.",
            "red_flag": "Sessions are frequently cancelled and not made up. You have no idea what goals are being worked on.",
            "ask": "Is this for articulation, language, fluency, or all three? Can you show me the baseline and where my child is now?",
            "color": "#2563EB",
        },
        {
            "name": "Occupational Therapy",
            "abbr": "OT",
            "what": "An Occupational Therapist helps your child with the fine motor and sensory skills needed for school — handwriting, cutting, using tools, managing sensory input, and daily activities like organizing their backpack or opening a lunch container.",
            "where": "Pull-out sessions or can be push-in for classroom-based activities.",
            "how_often": "Specified in IEP — often 1 to 2 times per week for 30 minutes.",
            "good_sign": "Therapist shares specific strategies you can use at home. Goals address real classroom challenges.",
            "red_flag": "OT goals are vague like 'improve fine motor skills' with no measurable target.",
            "ask": "What specific school activities is OT targeting? What can I do at home to support this?",
            "color": "#7C3AED",
        },
        {
            "name": "Physical Therapy",
            "abbr": "PT",
            "what": "A Physical Therapist addresses your child's ability to move safely in the school environment — walking, navigating stairs, PE participation, gross motor coordination, and physical endurance.",
            "where": "Usually in a gym, hallway, or therapy room.",
            "how_often": "Specified in IEP — frequency depends on need.",
            "good_sign": "Goals are specific to school participation. Therapist consults with PE teacher.",
            "red_flag": "PT only works on isolated exercises with no connection to school activities.",
            "ask": "How does PT connect to my child's participation in PE and recess? What are the functional goals?",
            "color": "#D97706",
        },
        {
            "name": "Counseling / Social Work",
            "abbr": "Counseling",
            "what": "A school psychologist or social worker provides counseling sessions to help your child with emotional regulation, social skills, coping strategies, anxiety, behavior, and mental health support.",
            "where": "Individual or small group sessions in a private office.",
            "how_often": "Specified in IEP — commonly 1 to 2 times per week.",
            "good_sign": "Counselor communicates with teachers and parents about strategies. Goals address specific behaviors or emotional needs documented in the IEP.",
            "red_flag": "You never hear from the counselor. No connection between counseling goals and classroom behavior.",
            "ask": "What specific skills or issues is counseling addressing? How are we coordinating across home and school?",
            "color": "#16A34A",
        },
        {
            "name": "Paraprofessional Support",
            "abbr": "Para / 1:1",
            "what": "A paraprofessional (teaching assistant) provides individualized support to your child. Can be 1:1 (assigned only to your child) or shared among a small group. The IEP must specify the level of support needed and why.",
            "where": "Wherever the student is — in class, at lunch, during transitions.",
            "how_often": "During the school day as specified in the IEP.",
            "good_sign": "The para supports your child's independence — helping them do things themselves, not doing things for them. There is a plan to reduce support over time if appropriate.",
            "red_flag": "The para does all the work for your child. No plan to build independence. Your child never interacts with the teacher directly.",
            "ask": "What is the para's role specifically? Is there a plan to fade the support over time? Is the para trained for my child's needs?",
            "color": "#E65100",
        },
    ],
}

# ── Tab per service category ──────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Special Education Instruction", "Related Services"])

def render_service(svc: dict):
    with st.expander(f"**{svc['abbr']}** — {svc['name']}", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:#F8FAFF;border-left:4px solid {svc['color']};
                        border-radius:8px;padding:14px;margin-bottom:10px;">
                <div style="font-weight:700;color:{svc['color']};font-size:0.82rem;
                            margin-bottom:6px;">WHAT IT IS</div>
                <div style="color:#334155;font-size:0.88rem;line-height:1.75;">{svc['what']}</div>
            </div>
            <div style="background:#F0FDF4;border-left:4px solid #16A34A;
                        border-radius:8px;padding:12px;margin-bottom:8px;">
                <div style="font-weight:700;color:#15803D;font-size:0.78rem;margin-bottom:4px;">WHERE</div>
                <div style="color:#334155;font-size:0.85rem;">{svc['where']}</div>
            </div>
            <div style="background:#EFF6FF;border-left:4px solid #2563EB;
                        border-radius:8px;padding:12px;">
                <div style="font-weight:700;color:#1D4ED8;font-size:0.78rem;margin-bottom:4px;">HOW OFTEN</div>
                <div style="color:#334155;font-size:0.85rem;">{svc['how_often']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#F0FDF4;border-left:4px solid #16A34A;
                        border-radius:8px;padding:12px;margin-bottom:8px;">
                <div style="font-weight:700;color:#15803D;font-size:0.78rem;margin-bottom:4px;">✅ GOOD SIGN</div>
                <div style="color:#334155;font-size:0.85rem;">{svc['good_sign']}</div>
            </div>
            <div style="background:#FFF1F2;border-left:4px solid #DC2626;
                        border-radius:8px;padding:12px;margin-bottom:8px;">
                <div style="font-weight:700;color:#DC2626;font-size:0.78rem;margin-bottom:4px;">🚩 RED FLAG</div>
                <div style="color:#334155;font-size:0.85rem;">{svc['red_flag']}</div>
            </div>
            <div style="background:#FFF8E1;border-left:4px solid #D97706;
                        border-radius:8px;padding:12px;">
                <div style="font-weight:700;color:#D97706;font-size:0.78rem;margin-bottom:4px;">❓ ASK THE TEAM</div>
                <div style="color:#334155;font-size:0.85rem;font-style:italic;">{svc['ask']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("pdf_loaded"):
            results = search_chunks([], svc["abbr"] + " " + svc["name"][:30], top_k=1)
            if results:
                r = results[0]
                st.markdown(f"""
                <div style="background:#F8FAFF;border-radius:6px;padding:10px 14px;
                            margin-top:8px;font-size:0.82rem;color:#334155;line-height:1.7;">
                    <b>📄 From your document (Page {r['page']}):</b><br>{r['text'][:300]}…
                </div>""", unsafe_allow_html=True)

with tab1:
    st.info("These are the main ways your child receives special education instruction. Your IEP must specify the type, frequency, duration, and location for each one.")
    for svc in SERVICES["Special Education Instruction"]:
        render_service(svc)

with tab2:
    st.info("Related services support your child in benefiting from their special education program. They are in addition to the main instruction.")
    for svc in SERVICES["Related Services"]:
        render_service(svc)
