"""
Page: Disability Classifications
All 13 IDEA disability categories explained in plain English.
Parent selects their child's classification and gets full details.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Disability Classifications · IEP Guide", page_icon="📊", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("📊", "Disability Classifications", "All 13 IDEA disability categories explained in plain English — select your child's classification below", "#DC2626")
status_banner()

CLASSIFICATIONS = {
    "Autism Spectrum Disorder": {
        "abbr": "ASD", "color": "#2563EB",
        "plain": "A developmental disability that affects how a person communicates, interacts with others, and experiences the world. It is a spectrum — every person with autism is different.",
        "school_impact": "May affect ability to communicate in class, manage sensory input (noise, lights, textures), follow social cues, handle transitions between activities, and engage with group work.",
        "common_services": ["Speech-Language Therapy", "Occupational Therapy", "SETSS or Special Class", "Counseling", "ABA (if appropriate)"],
        "key_rights": ["FBA and BIP must be considered if behavior affects learning", "Sensory needs must be addressed in the IEP", "AAC devices must be considered if speech is limited"],
        "questions": ["Does the IEP address communication AND social needs?", "Has a sensory assessment been done?", "Is ESY (summer services) being considered?"],
        "sopm_pages": "Pages 24, 52",
    },
    "Learning Disability": {
        "abbr": "LD / SLD", "color": "#7C3AED",
        "plain": "A specific difficulty processing information in one or more academic areas — most commonly reading (dyslexia), writing (dysgraphia), or math (dyscalculia). It is not related to intelligence.",
        "school_impact": "Difficulty reading grade-level text, writing organized paragraphs, doing math calculations, following multi-step directions, or processing written/spoken information at the same pace as peers.",
        "common_services": ["SETSS (reading or math focus)", "ICT or Resource Room", "Reading specialist", "Assistive technology (text-to-speech, spell-check)"],
        "key_rights": ["Multiple assessment tools must be used — not just an IQ test", "RTI data should be included in the evaluation", "Extended time and read-aloud are common and valid accommodations"],
        "questions": ["Which specific area — reading, writing, or math?", "What is the baseline score and target for each goal?", "Is assistive technology being provided?"],
        "sopm_pages": "Pages 52–54",
    },
    "Emotional Disturbance": {
        "abbr": "ED", "color": "#DC2626",
        "plain": "A condition in which emotional or behavioral difficulties significantly affect a student's ability to learn. This is not about bad behavior — it is about a real disability that affects school performance.",
        "school_impact": "Difficulty regulating emotions in class, maintaining relationships with peers or teachers, managing anxiety or depression, staying focused, or behaving consistently across settings.",
        "common_services": ["Counseling (individual and/or group)", "Social work services", "Special Class if needed", "Crisis intervention plan"],
        "key_rights": ["FBA must be done before a BIP is written", "Manifestation Determination Review required before long-term suspension", "Trauma history must be considered in the evaluation"],
        "questions": ["Has an FBA been completed?", "Does the IEP include a Behavioral Intervention Plan?", "Is the school using trauma-informed approaches?"],
        "sopm_pages": "Pages 52–53",
    },
    "Intellectual Disability": {
        "abbr": "ID", "color": "#D97706",
        "plain": "Significant limitations in intellectual functioning (thinking, learning, problem-solving) AND adaptive behavior (daily living skills) that began before age 18.",
        "school_impact": "Difficulty with academic content at grade level, applying skills to new situations, independent daily living tasks, and complex multi-step activities.",
        "common_services": ["Special Class (often 12:1:1 or 8:1:1)", "Life skills instruction", "Vocational training (age 14+)", "Community-based instruction"],
        "key_rights": ["Both IQ AND adaptive behavior must be assessed — not just IQ", "Transition planning must begin by age 15 (NYC)", "Community-based instruction is a valid and appropriate service"],
        "questions": ["Was adaptive behavior assessed with a standardized tool (Vineland, ABAS)?", "Is transition planning included in the IEP?", "What vocational goals are being developed?"],
        "sopm_pages": "Pages 52, 57",
    },
    "Speech or Language Impairment": {
        "abbr": "SLI", "color": "#16A34A",
        "plain": "A communication disorder that affects how a person speaks, understands language, uses language, or both. The most common disability classification in schools.",
        "school_impact": "Difficulty being understood when speaking, understanding spoken instructions, organizing thoughts into spoken or written language, or reading (when tied to language processing).",
        "common_services": ["Speech-Language Therapy — individual and/or group"],
        "key_rights": ["Must be evaluated by an ASHA-certified Speech-Language Pathologist", "Therapy must specify type — articulation, language, fluency, or voice", "AAC must be considered if speech is severely limited"],
        "questions": ["Is this for articulation, language comprehension, or expressive language?", "What are the baseline scores?", "How will I know if my child is making progress?"],
        "sopm_pages": "Pages 24, 52",
    },
    "Other Health Impairment": {
        "abbr": "OHI", "color": "#0891B2",
        "plain": "A health condition that limits a student's strength, vitality, or alertness and adversely affects educational performance. ADHD is the most common reason for this classification.",
        "school_impact": "Limited attention span, difficulty staying on task, fatigue, impulsivity, difficulty following multi-step directions, or missing school due to medical appointments or illness.",
        "common_services": ["Accommodations (extended time, preferential seating, breaks)", "Resource Room or SETSS if academic support is needed", "Counseling for coping strategies"],
        "key_rights": ["Medical documentation from a physician is required", "If special education is not needed, a 504 Plan may be more appropriate", "ADHD alone does not automatically qualify for an IEP — it must affect educational performance"],
        "questions": ["What specific health condition is documented?", "Is special education actually needed, or would a 504 Plan be sufficient?", "What accommodations are in the IEP?"],
        "sopm_pages": "Pages 52, 54",
    },
    "Deafness": {
        "abbr": "D", "color": "#9333EA",
        "plain": "A hearing loss so severe that a student cannot process spoken language, with or without amplification, affecting educational performance.",
        "school_impact": "Cannot access verbal instruction without specialized support. Needs visual or tactile learning approaches and communication access throughout the school day.",
        "common_services": ["Teacher of the Deaf and Hearing Impaired", "Sign language interpreter", "FM system or captioning", "Speech-Language Therapy"],
        "key_rights": ["Communication needs must be assessed and addressed in the IEP", "Full access to communication in the classroom is required", "Parent communication preferences must be considered"],
        "questions": ["Is the student using ASL, oral communication, or both?", "Is a qualified interpreter provided in all settings?", "Are all teachers trained to work with deaf students?"],
        "sopm_pages": "Pages 49, 52",
    },
    "Hearing Impairment": {
        "abbr": "HI", "color": "#0D9488",
        "plain": "A hearing loss that adversely affects educational performance but is not as severe as deafness. The student can process some spoken language, often with amplification.",
        "school_impact": "Difficulty hearing in noisy classrooms, understanding instructions from a distance, participating in group discussions, and processing spoken information accurately.",
        "common_services": ["FM system or hearing loop", "Preferential seating", "Speech-Language Therapy", "Teacher of the Deaf and Hearing Impaired as needed"],
        "key_rights": ["Audiological assessment must be part of the evaluation", "Classroom acoustics must be considered", "Hearing aids or FM systems must be accommodated"],
        "questions": ["Has a recent audiological evaluation been done?", "Does the classroom have appropriate acoustics or an FM system?", "Is the student's hearing aid functioning and checked daily?"],
        "sopm_pages": "Pages 29, 52–53",
    },
    "Visual Impairment Including Blindness": {
        "abbr": "VI", "color": "#E65100",
        "plain": "A visual impairment — even when corrected with glasses or contacts — that adversely affects educational performance.",
        "school_impact": "Difficulty accessing print materials, seeing the board, navigating the classroom, and participating in activities that rely on vision.",
        "common_services": ["Teacher of the Visually Impaired", "Braille instruction (if needed)", "Orientation and Mobility services", "Large print or digital materials", "Assistive technology"],
        "key_rights": ["Braille instruction must be provided if appropriate", "All materials must be provided in accessible format", "Orientation and Mobility is a required related service when needed"],
        "questions": ["Is the student being taught Braille if vision loss is significant?", "Are all materials available in accessible format?", "Is Orientation and Mobility included?"],
        "sopm_pages": "Page 49, 52",
    },
    "Orthopedic Impairment": {
        "abbr": "OI", "color": "#854D0E",
        "plain": "A physical impairment caused by a congenital anomaly, disease, or other cause that adversely affects educational performance.",
        "school_impact": "Difficulty accessing classrooms, writing, using standard equipment, participating in PE, or managing fatigue from physical effort required to get through the school day.",
        "common_services": ["Physical Therapy", "Occupational Therapy", "Assistive technology", "Accessible facilities and equipment"],
        "key_rights": ["School must be physically accessible", "Assistive technology must be considered", "Adaptive Physical Education must be provided if needed"],
        "questions": ["Is the school building fully accessible for my child?", "Are all necessary assistive devices available and maintained?", "Is Adaptive PE included?"],
        "sopm_pages": "Page 52, 54",
    },
    "Traumatic Brain Injury": {
        "abbr": "TBI", "color": "#7F1D1D",
        "plain": "An acquired injury to the brain caused by an external physical force — resulting in total or partial functional disability, or psychosocial impairment.",
        "school_impact": "Memory difficulties, fatigue, difficulty processing information quickly, emotional regulation challenges, and varying performance day to day.",
        "common_services": ["Special Class or Resource Room", "Counseling", "OT and/or PT", "Extended time and reduced assignments"],
        "key_rights": ["Medical documentation of the injury is required", "The IEP must address the variable nature of TBI — good days and hard days", "Fatigue management must be built into the school day"],
        "questions": ["Does the IEP address fatigue and variable performance?", "Are rest breaks built into the schedule?", "Is the team aware of how TBI symptoms change over time?"],
        "sopm_pages": "Page 52",
    },
    "Multiple Disabilities": {
        "abbr": "MD", "color": "#4A1B9A",
        "plain": "The simultaneous presence of two or more disabilities (such as intellectual disability combined with blindness or physical disability) where the combination causes such severe educational needs that a single disability program cannot accommodate them.",
        "school_impact": "Complex and intensive needs across multiple areas — physical, communication, cognitive, behavioral, and daily living skills.",
        "common_services": ["Intensive special class (6:1:1 or similar)", "Multiple related services", "Assistive technology", "Life skills and community-based instruction"],
        "key_rights": ["The IEP must address all disability areas — not just the primary one", "Related services must be coordinated and work together", "Transition planning is critical and should begin early"],
        "questions": ["Does the IEP address ALL disability areas?", "Are all service providers communicating with each other?", "Is the placement the least restrictive one that meets all needs?"],
        "sopm_pages": "Page 52",
    },
    "Deaf-Blindness": {
        "abbr": "DB", "color": "#1E3A5F",
        "plain": "The combination of hearing and visual impairments that causes such severe communication and other developmental and educational needs that programs for students with just deafness or just blindness cannot accommodate them.",
        "school_impact": "Requires highly specialized communication systems, intensive 1:1 support, and adapted environment across all aspects of the school day.",
        "common_services": ["Intervener services (specialized 1:1 support)", "Augmentative communication", "Orientation and Mobility", "Teacher of the Deaf-Blind"],
        "key_rights": ["Intervener services are critical and must be provided", "All communication must be accessible", "Specialized expertise is required — district must ensure qualified staff"],
        "questions": ["Is the school providing a qualified intervener?", "Is the student's communication system fully supported?", "Does the district have staff trained in deaf-blindness?"],
        "sopm_pages": "Page 52",
    },
}

# ── Layout ────────────────────────────────────────────────────────────────────
st.info("There are 13 disability categories under IDEA. Your child must qualify under at least one to receive an IEP. Understanding the classification helps you understand what services should be in the IEP.")

selected = st.selectbox(
    "Select your child's disability classification",
    ["— Select a classification —"] + list(CLASSIFICATIONS.keys()),
    label_visibility="visible",
)

if selected != "— Select a classification —":
    cls   = CLASSIFICATIONS[selected]
    color = cls["color"]

    # Header card
    st.markdown(f"""
    <div style="background:{color};border-radius:14px;padding:20px 24px;margin:16px 0;">
        <div style="font-family:'Nunito',sans-serif;font-weight:900;
                    color:white;font-size:1.4rem;margin-bottom:4px;">
            {selected}</div>
        <div style="color:rgba(255,255,255,0.85);font-size:0.85rem;font-family:'Nunito',sans-serif;font-weight:600;">
            Abbreviation: {cls['abbr']} · SOPM reference: {cls['sopm_pages']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Plain English
        st.markdown(f"""
        <div style="background:#F8FAFF;border-left:4px solid {color};
                    border-radius:8px;padding:16px;margin-bottom:12px;">
            <div style="font-weight:800;color:{color};font-size:0.82rem;
                        text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;">
                What This Means in Plain English</div>
            <div style="color:#334155;font-size:0.9rem;line-height:1.8;">{cls['plain']}</div>
        </div>
        """, unsafe_allow_html=True)

        # School impact
        st.markdown(f"""
        <div style="background:#FFF8E1;border-left:4px solid #D97706;
                    border-radius:8px;padding:14px;margin-bottom:12px;">
            <div style="font-weight:800;color:#D97706;font-size:0.82rem;
                        text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;">
                How It Affects School</div>
            <div style="color:#334155;font-size:0.88rem;line-height:1.8;">{cls['school_impact']}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Common services
        st.markdown(f"""
        <div style="background:#F0FDF4;border-left:4px solid #16A34A;
                    border-radius:8px;padding:14px;margin-bottom:12px;">
            <div style="font-weight:800;color:#15803D;font-size:0.82rem;
                        text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;">
                Common Services for This Classification</div>
        """, unsafe_allow_html=True)
        for svc in cls["common_services"]:
            st.markdown(f"""
            <div style="background:white;border-radius:6px;padding:6px 12px;
                        margin-bottom:5px;font-size:0.86rem;color:#166534;
                        border:1px solid #BBF7D0;">✓ {svc}</div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Key rights
        st.markdown(f"""
        <div style="background:#FFF1F2;border-left:4px solid #DC2626;
                    border-radius:8px;padding:14px;margin-bottom:12px;">
            <div style="font-weight:800;color:#DC2626;font-size:0.82rem;
                        text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;">
                Your Key Rights for This Classification</div>
        """, unsafe_allow_html=True)
        for right in cls["key_rights"]:
            st.markdown(f'<div style="font-size:0.86rem;color:#7F1D1D;padding:4px 0;line-height:1.6;">🛡️ {right}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Questions to ask
    st.markdown(f"""
    <div style="background:#EFF6FF;border-radius:10px;padding:16px;margin-top:4px;">
        <div style="font-weight:800;color:#1E40AF;font-size:0.88rem;margin-bottom:10px;">
            ❓ Questions to Ask at the IEP Meeting</div>
    """, unsafe_allow_html=True)
    for q in cls["questions"]:
        st.markdown(f'<div style="background:white;border-radius:6px;padding:8px 12px;margin-bottom:6px;font-size:0.87rem;color:#1E3A8A;border:1px solid #BFDBFE;">"{q}"</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # From PDF
    if st.session_state.get("pdf_loaded"):
        st.markdown("---")
        with st.expander(f"What your document says about {selected}"):
            results = search_chunks([], selected + " " + cls["abbr"] + " disability classification", top_k=3)
            for r in results:
                st.markdown(f"""
                <div style="background:#F8FAFF;border-left:3px solid {color};
                            border-radius:6px;padding:10px 14px;margin-bottom:8px;
                            font-size:0.85rem;color:#334155;line-height:1.75;">
                    <b>Page {r['page']} · {r['section']}</b><br>{r['text'][:400]}…
                </div>""", unsafe_allow_html=True)
else:
    # Show all as overview grid
    st.markdown("### All 13 Classifications at a Glance")
    cols = st.columns(3)
    for i, (name, cls) in enumerate(CLASSIFICATIONS.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;border:1px solid #E2E8F0;
                        border-left:4px solid {cls['color']};padding:12px 14px;
                        margin-bottom:10px;">
                <div style="font-family:'Nunito',sans-serif;font-weight:800;
                            color:{cls['color']};font-size:0.8rem;">{cls['abbr']}</div>
                <div style="font-weight:600;color:#1E293B;font-size:0.85rem;
                            margin:3px 0;">{name}</div>
                <div style="color:#64748B;font-size:0.78rem;line-height:1.5;">
                    {cls['plain'][:90]}…</div>
            </div>
            """, unsafe_allow_html=True)
