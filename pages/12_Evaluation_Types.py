"""
Page: Evaluation Types
All 12 evaluation types from SOPM pages 24-37 explained clearly.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Evaluation Types · IEP Guide", page_icon="🔍", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("🔍", "Evaluation Types Explained", "The SOPM describes 12 different evaluations — what each one tests, who conducts it, and when to request it", "#16A34A")
status_banner()

st.info("When your child is referred for special education, the school must evaluate every area of suspected disability. Here are all the evaluation types described in the SOPM and what each one means.")

EVALS = [
    {"name":"Psychoeducational Assessment","abbr":"Psych","color":"#2563EB","sopm":"Pages 24–25",
     "what":"The core evaluation done by a school psychologist. Tests cognitive ability (IQ), processing speed, working memory, and academic achievement. This is almost always part of an initial evaluation.",
     "who":"Licensed School Psychologist",
     "tests":"IQ tests (WISC, Stanford-Binet), achievement tests (WIAT, WJ), processing assessments",
     "tells_us":"Whether there is a significant gap between your child's ability and their achievement — the core measure for Learning Disability. Also identifies cognitive strengths and weaknesses.",
     "request_when":"Almost always required. Especially for Learning Disability, Intellectual Disability, Autism, Emotional Disturbance."},
    {"name":"Speech and Language Assessment","abbr":"SLP Eval","color":"#0D9488","sopm":"Pages 24–25",
     "what":"Evaluates how your child communicates — both understanding language (receptive) and using language (expressive). Also tests articulation (how clearly they speak) and fluency.",
     "who":"Licensed Speech-Language Pathologist (ASHA certified)",
     "tests":"CELF, PPVT, Goldman-Fristoe, language sampling, articulation tests",
     "tells_us":"Whether a speech or language impairment exists and its severity. Whether therapy is needed and what type.",
     "request_when":"When your child has difficulty being understood, following verbal directions, organizing thoughts, or communicating with peers."},
    {"name":"Occupational Therapy Assessment","abbr":"OT Eval","color":"#7C3AED","sopm":"Page 25",
     "what":"Evaluates fine motor skills, sensory processing, visual-motor integration, handwriting, self-care skills, and ability to manage the school environment.",
     "who":"Licensed Occupational Therapist",
     "tests":"Beery VMI, Bruininks, sensory processing checklists, handwriting samples, classroom observation",
     "tells_us":"Whether OT services are needed and for what specific skills. Identifies sensory sensitivities that affect learning.",
     "request_when":"When your child has difficulty with handwriting, cutting, using tools, sensory regulation, or daily self-care tasks."},
    {"name":"Physical Therapy Assessment","abbr":"PT Eval","color":"#D97706","sopm":"Page 25",
     "what":"Evaluates gross motor skills, balance, coordination, mobility in the school environment, endurance, and physical ability to access all areas of the school.",
     "who":"Licensed Physical Therapist",
     "tests":"BOTMP, movement observation, functional mobility assessment",
     "tells_us":"Whether PT services are needed to help the student access the educational environment.",
     "request_when":"When your child has difficulty walking, climbing stairs, participating in PE, or safely navigating the school building."},
    {"name":"Functional Behavioral Assessment","abbr":"FBA","color":"#DC2626","sopm":"Pages 26–28",
     "what":"Analyzes why a challenging behavior occurs — what triggers it, what the student gets from it, and in what settings it happens. This must be done BEFORE writing a Behavioral Intervention Plan (BIP).",
     "who":"School psychologist, special education teacher, or behavior specialist",
     "tests":"Direct observation, ABC (Antecedent-Behavior-Consequence) data, interviews with teachers and parents",
     "tells_us":"The function of the behavior (escape, attention, sensory, access to items). This guides what positive strategies will actually work.",
     "request_when":"When your child's behavior is affecting their learning or others' learning, before any BIP is written, or if the school wants to change your child's placement due to behavior."},
    {"name":"Audiological Assessment","abbr":"Audiology","color":"#0891B2","sopm":"Page 29",
     "what":"Tests your child's hearing — type and degree of hearing loss, impact on understanding speech, and whether hearing aids or FM systems would help.",
     "who":"Licensed Audiologist",
     "tests":"Pure tone audiogram, speech audiometry, tympanometry, acoustic reflex testing",
     "tells_us":"Whether a hearing impairment exists and its impact on educational performance.",
     "request_when":"When your child has difficulty hearing in class, doesn't respond to their name, frequently asks for repetition, or has a history of ear infections."},
    {"name":"Assistive Technology Assessment","abbr":"AT Eval","color":"#16A34A","sopm":"Pages 29, 65",
     "what":"Evaluates whether assistive technology devices or services would help your child access education. Every student's IEP team must consider AT — this formal evaluation goes deeper.",
     "who":"AT specialist or trained special education staff",
     "tests":"Trial use of AT devices, observation, review of curriculum demands, student preference",
     "tells_us":"What specific tools — text-to-speech, AAC devices, word prediction software, alternative keyboards — would help your child participate and learn.",
     "request_when":"When your child has difficulty with reading, writing, communication, or accessing materials in the standard format."},
    {"name":"Vocational Assessment","abbr":"Voc Eval","color":"#E65100","sopm":"Page 25",
     "what":"Evaluates work-related interests, aptitudes, and skills to inform transition planning. Looks at what kinds of work environments and tasks a student is suited for.",
     "who":"Vocational evaluator or school counselor",
     "tests":"Interest inventories, aptitude assessments, work samples, observation",
     "tells_us":"A student's vocational interests and strengths to guide post-secondary employment goals in the IEP.",
     "request_when":"For students age 14+ as part of transition planning. Required to develop meaningful post-secondary employment goals."},
    {"name":"Neuropsychological Assessment","abbr":"Neuropsych","color":"#9333EA","sopm":"Page 29",
     "what":"A comprehensive evaluation of brain-behavior relationships — how the brain's functioning affects attention, memory, executive function, processing, and behavior. More detailed than a standard psychoeducational.",
     "who":"Licensed Neuropsychologist (doctoral level)",
     "tests":"Extensive battery covering memory, attention, executive function, processing, language, and motor skills",
     "tells_us":"The underlying cognitive profile in depth — often identifies patterns not visible in standard testing. Especially useful for TBI, complex profiles, or after a standard evaluation doesn't explain the full picture.",
     "request_when":"When standard testing hasn't explained why the child is struggling, after a traumatic brain injury, or when there are complex co-occurring diagnoses."},
    {"name":"Psychiatric Assessment","abbr":"Psych Eval (Psychiatric)","color":"#7F1D1D","sopm":"Page 29",
     "what":"A medical evaluation by a psychiatrist to assess mental health conditions, medication needs, and diagnosis. Different from the school psychoeducational assessment.",
     "who":"Licensed Psychiatrist (medical doctor)",
     "tests":"Clinical interview, behavioral rating scales, diagnostic criteria review, medication review",
     "tells_us":"Whether a psychiatric diagnosis exists, whether medication may be appropriate, and how mental health conditions affect school functioning.",
     "request_when":"When Emotional Disturbance is suspected, when existing mental health diagnoses need to be documented, or when medication is being considered."},
    {"name":"Neurological Assessment","abbr":"Neuro Eval","color":"#1E3A5F","sopm":"Page 29",
     "what":"A medical evaluation by a neurologist to assess neurological functioning — brain activity, seizures, motor disorders, or neurological conditions affecting learning.",
     "who":"Licensed Neurologist (medical doctor)",
     "tests":"Physical and neurological examination, EEG if needed, medical history review",
     "tells_us":"Whether a neurological condition is present and how it affects the student's educational needs.",
     "request_when":"When seizures are suspected, when there is a known neurological condition, or when other evaluations suggest a possible neurological basis for the student's needs."},
    {"name":"Bilingual or Translated Assessment","abbr":"Bilingual Eval","color":"#065F46","sopm":"Pages 34–37",
     "what":"Required when a student's primary language is not English. Evaluations must be conducted in the student's native language when feasible. Standard tests translated informally are not acceptable.",
     "who":"Bilingual evaluator or qualified interpreter working with evaluator",
     "tests":"Standardized assessments in native language, or non-verbal assessments, depending on language availability",
     "tells_us":"Whether the difficulty is a disability or a language acquisition issue. Critical distinction — many students are misidentified as having disabilities when they are actually English language learners.",
     "request_when":"When the student's first language is not English, when the student is an English Language Learner, or when a standard English assessment may not accurately reflect the student's abilities."},
]

# ── View toggle ───────────────────────────────────────────────────────────────
view = st.radio("View", ["All Evaluations", "Search by concern"], horizontal=True)

if view == "Search by concern":
    concern = st.selectbox("My child has difficulty with…", [
        "— Select a concern —",
        "Reading or writing",
        "Math",
        "Speaking or being understood",
        "Hearing in class",
        "Handwriting or fine motor skills",
        "Moving around the school / gross motor",
        "Behavior or emotional regulation",
        "Attention or focus",
        "Communicating at all (non-verbal)",
        "Work and future planning (age 14+)",
        "Coming from a different language background",
    ])
    concern_map = {
        "Reading or writing": ["Psychoeducational Assessment","Speech and Language Assessment","Assistive Technology Assessment","Bilingual or Translated Assessment"],
        "Math": ["Psychoeducational Assessment","Assistive Technology Assessment"],
        "Speaking or being understood": ["Speech and Language Assessment","Audiological Assessment","Assistive Technology Assessment"],
        "Hearing in class": ["Audiological Assessment","Assistive Technology Assessment"],
        "Handwriting or fine motor skills": ["Occupational Therapy Assessment","Assistive Technology Assessment"],
        "Moving around the school / gross motor": ["Physical Therapy Assessment"],
        "Behavior or emotional regulation": ["Functional Behavioral Assessment","Psychoeducational Assessment","Psychiatric Assessment"],
        "Attention or focus": ["Psychoeducational Assessment","Psychiatric Assessment","Functional Behavioral Assessment"],
        "Communicating at all (non-verbal)": ["Speech and Language Assessment","Assistive Technology Assessment","Audiological Assessment"],
        "Work and future planning (age 14+)": ["Vocational Assessment","Neuropsychological Assessment"],
        "Coming from a different language background": ["Bilingual or Translated Assessment","Speech and Language Assessment"],
    }
    if concern != "— Select a concern —":
        recommended = concern_map.get(concern, [])
        st.markdown(f"""
        <div style="background:#EFF6FF;border-radius:10px;padding:12px 16px;margin:10px 0 16px;">
            <b style="color:#1E40AF;">Recommended evaluations for "{concern}":</b>
            <div style="color:#1E3A8A;font-size:0.87rem;margin-top:4px;">
                {' · '.join(recommended)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        show_evals = [e for e in EVALS if e["name"] in recommended]
    else:
        show_evals = []
else:
    show_evals = EVALS

for ev in show_evals:
    color = ev["color"]
    with st.expander(f"**{ev['abbr']}** — {ev['name']}   ·   {ev['sopm']}"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:{color}0D;border-left:4px solid {color};
                        border-radius:8px;padding:13px;margin-bottom:10px;">
                <div style="font-weight:700;color:{color};font-size:0.8rem;margin-bottom:5px;">WHAT IT EVALUATES</div>
                <div style="color:#334155;font-size:0.87rem;line-height:1.75;">{ev['what']}</div>
            </div>
            <div style="background:#F8FAFF;border-radius:8px;padding:11px;margin-bottom:8px;">
                <div style="font-weight:700;color:#475569;font-size:0.78rem;margin-bottom:4px;">WHO CONDUCTS IT</div>
                <div style="color:#334155;font-size:0.85rem;">{ev['who']}</div>
            </div>
            <div style="background:#F0F9FF;border-radius:8px;padding:11px;">
                <div style="font-weight:700;color:#0369A1;font-size:0.78rem;margin-bottom:4px;">COMMON TESTS USED</div>
                <div style="color:#334155;font-size:0.84rem;">{ev['tests']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#F0FDF4;border-radius:8px;padding:11px;margin-bottom:8px;">
                <div style="font-weight:700;color:#15803D;font-size:0.78rem;margin-bottom:4px;">WHAT IT TELLS US</div>
                <div style="color:#334155;font-size:0.85rem;line-height:1.7;">{ev['tells_us']}</div>
            </div>
            <div style="background:#FFF8E1;border-radius:8px;padding:11px;">
                <div style="font-weight:700;color:#D97706;font-size:0.78rem;margin-bottom:4px;">REQUEST THIS WHEN</div>
                <div style="color:#334155;font-size:0.85rem;line-height:1.7;">{ev['request_when']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("pdf_loaded"):
            results = search_chunks([], ev["name"] + " assessment evaluation", top_k=1)
            if results:
                r = results[0]
                st.markdown(f"""
                <div style="background:#F8FAFF;border-left:3px solid {color};
                            border-radius:6px;padding:9px 13px;margin-top:6px;
                            font-size:0.82rem;color:#334155;line-height:1.7;">
                    <b>📄 Page {r['page']}:</b> {r['text'][:280]}…</div>""", unsafe_allow_html=True)
