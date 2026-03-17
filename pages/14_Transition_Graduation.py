"""
Page: Transition & Graduation
For families of students age 14+. SOPM pages 57, 122-124.
Diploma options, CDOS, exit summary, transition services.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Transition & Graduation · IEP Guide", page_icon="🎓", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("🎓", "Transition & Graduation Guide", "For families of students age 14 and older — planning for life after school and graduation options", "#16A34A")
status_banner()

st.info("**Transition planning** is required in every IEP for students age 15 (and many districts begin at 14). It prepares your child for life after high school — college, work, and independent living. Graduation options for students with IEPs are broader than most parents realize.")

tab_transition, tab_diplomas, tab_exit, tab_rights = st.tabs([
    "Transition Planning", "Diploma Options", "Exit Summary", "Your Rights"
])

with tab_transition:
    st.markdown("### What Is Transition Planning?")
    st.markdown("""
    <div style="background:#F0FDF4;border-left:4px solid #16A34A;border-radius:8px;
                padding:14px;margin-bottom:16px;font-size:0.9rem;color:#166534;line-height:1.75;">
        Transition planning is the process of helping your child move from school to adult life.
        It must be included in the IEP beginning at age 15 (IDEA requirement) — and NYC DOE recommends
        starting conversations at age 14. It covers three areas: further education/training,
        employment, and (when appropriate) independent living.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### The Three Required Transition Areas")
    areas = [
        ("🎓", "Education / Training After High School", "#2563EB",
         "Does your child plan to attend college, a vocational training program, a community college, or other post-secondary education? The IEP must include a measurable goal in this area.",
         ["College (2-year or 4-year)", "Vocational/trade school", "Job training program", "Adult continuing education", "Military service (if appropriate)"]),
        ("💼", "Employment", "#D97706",
         "What kind of work is your child interested in and suited for? The IEP must include a measurable employment goal based on age-appropriate assessments and the student's interests and strengths.",
         ["Competitive integrated employment", "Supported employment", "Sheltered workshop (though less preferred)", "Self-employment", "Volunteer work as a stepping stone"]),
        ("🏠", "Independent Living (when appropriate)", "#7C3AED",
         "Can your child manage daily living independently — transportation, money management, cooking, accessing community resources? This area is required when the disability affects independent living skills.",
         ["Living independently", "Supported living arrangement", "Living with family with support", "Money management skills", "Community navigation and transportation"]),
    ]

    for icon, area, color, desc, options in areas:
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-left:5px solid {color};
                    border-radius:10px;padding:16px 18px;margin-bottom:10px;">
            <div style="font-size:1.3rem;margin-bottom:6px;">{icon}</div>
            <div style="font-weight:800;color:{color};font-size:0.95rem;margin-bottom:8px;">{area}</div>
            <div style="color:#475569;font-size:0.87rem;line-height:1.7;margin-bottom:10px;">{desc}</div>
            <div style="font-weight:700;color:#374151;font-size:0.8rem;margin-bottom:6px;">Examples:</div>
            <div style="display:flex;flex-wrap:wrap;gap:6px;">
                {" ".join('<span style="background:' + color + '12;color:' + color + ';border-radius:6px;padding:3px 10px;font-size:0.78rem;font-weight:600;">' + o + '</span>' for o in options)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Transition Services in the IEP")
    st.markdown("""
    The IEP must specify what **transition services** will help your child reach their post-secondary goals.
    These are not just goals — they are actual services, activities, and experiences.
    """)
    services = [
        ("Vocational assessment", "Formal evaluation of interests, strengths and work readiness"),
        ("Work-based learning", "Internships, job shadowing, community work experience"),
        ("Career counseling", "Guidance on career pathways and post-secondary options"),
        ("Life skills instruction", "Cooking, budgeting, transportation, apartment living"),
        ("College prep support", "SAT/ACT prep, application assistance, campus visits"),
        ("Agency linkages", "Connecting to ACCES-VR (adult vocational rehab), OPWDD, other adult services"),
        ("Self-advocacy training", "Teaching the student to understand their disability and advocate for themselves"),
    ]
    for svc, desc in services:
        st.markdown(f"""
        <div style="display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #F1F5F9;
                    font-size:0.86rem;">
            <span style="color:#16A34A;font-weight:700;min-width:200px;">{svc}</span>
            <span style="color:#64748B;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Questions to Ask at the Transition IEP Meeting")
    qs = [
        "Has my child had a vocational assessment? If not, can we schedule one?",
        "What are my child's post-secondary goals based on their own stated interests?",
        "What transition services are included in the IEP and who will provide them?",
        "Is the school connecting my child to ACCES-VR or other adult services?",
        "What diploma track is my child on and is it appropriate for their goals?",
        "Does my child understand their disability and how to ask for accommodations in adult life?",
    ]
    for q in qs:
        st.markdown(f'<div style="background:#F0FDF4;border-radius:6px;padding:7px 12px;margin-bottom:5px;font-size:0.86rem;color:#166534;">❓ {q}</div>', unsafe_allow_html=True)

with tab_diplomas:
    st.markdown("### Graduation & Diploma Options in New York State")
    st.info("Students with IEPs have more diploma and credential options than most parents know. Understanding these early helps your child aim for the right path.")

    diplomas = [
        {"name":"Regents Diploma","color":"#2563EB","requirement":"Pass required Regents exams with scores of 65 or higher","for_iep":"Students with IEPs can use testing accommodations (extended time, separate location, read-aloud). Some students with IEPs pursue the full Regents Diploma.","note":"This is the standard diploma. Most colleges require it or its equivalent."},
        {"name":"Regents Diploma with Advanced Designation","color":"#7C3AED","requirement":"Pass additional Regents exams — meets higher standards","for_iep":"Available to students with IEPs who meet the requirements. Demonstrates college readiness.","note":"Opens more college options. Not required but a strong achievement."},
        {"name":"Local Diploma (Safety Net)","color":"#D97706","requirement":"Pass Regents exams with scores of 55–64 (lower passing standard, called the safety net)","for_iep":"Available ONLY to students with IEPs. The IEP must specifically document this option. Requires the student to take the exam but allows a lower passing score.","note":"Still a valid New York State diploma. Accepted by many employers and some colleges."},
        {"name":"CDOS Commencement Credential","color":"#16A34A","requirement":"Complete a Career Development and Occupational Studies (CDOS) program — work readiness, employability, and career/technical coursework","for_iep":"Specifically designed for students with disabilities. Can be earned instead of or alongside a diploma. Recognized by employers.","note":"Not a diploma — a credential. Students who earn CDOS but not a diploma may still receive a Skills and Achievement Commencement Credential."},
        {"name":"Skills and Achievement Commencement Credential","color":"#E65100","requirement":"For students who are not eligible for a diploma — demonstrates functional academic achievement and life skills","for_iep":"Specifically for students with significant disabilities who complete their IEP goals but do not meet diploma requirements.","note":"Recognized as completion of a school program. Comes with an Exit Summary detailing the student's strengths and needs."},
        {"name":"IEP Diploma (Discontinued in NY)","color":"#94A3B8","requirement":"N/A — no longer issued in New York State","for_iep":"New York discontinued IEP diplomas. If someone mentions an IEP diploma, clarify that NY now uses the CDOS and Skills credentials instead.","note":"This is outdated. If your child's team mentions an IEP diploma, ask for clarification."},
    ]

    for d in diplomas:
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-left:5px solid {d['color']};
                    border-radius:10px;padding:14px 18px;margin-bottom:10px;">
            <div style="font-weight:800;color:{d['color']};font-size:0.95rem;margin-bottom:10px;">{d['name']}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;font-size:0.84rem;">
                <div><div style="font-weight:700;color:#374151;margin-bottom:4px;">Requirement</div>
                     <div style="color:#64748B;">{d['requirement']}</div></div>
                <div><div style="font-weight:700;color:#374151;margin-bottom:4px;">For Students with IEPs</div>
                     <div style="color:#64748B;">{d['for_iep']}</div></div>
                <div><div style="font-weight:700;color:#374151;margin-bottom:4px;">Important Note</div>
                     <div style="color:#64748B;">{d['note']}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_exit:
    st.markdown("### The Exit Summary")
    st.markdown("""
    <div style="background:#EFF6FF;border-left:4px solid #2563EB;border-radius:8px;
                padding:14px;margin-bottom:14px;font-size:0.9rem;color:#1E3A8A;line-height:1.75;">
        When a student with a disability graduates or ages out of school (at age 21), the school
        must provide an <b>Exit Summary</b>. This document summarizes the student's academic
        achievement and functional performance and includes recommendations to help the student
        meet their post-secondary goals.
    </div>
    """, unsafe_allow_html=True)

    exit_items = [
        ("What it contains", ["Summary of the student's present levels of academic achievement", "Summary of functional performance (daily living, social, behavioral)", "Recommendations for accommodations and supports in adult life", "Statement of the student's post-secondary goals", "Information about transition services accessed during school"]),
        ("Why it matters", ["It follows your child into adult life — colleges, employers, and adult service agencies may ask for it", "Documents what supports the student needs — so they don't have to start over explaining their history", "Can be used to apply for disability accommodations at college (Americans with Disabilities Act)", "Supports applications to ACCES-VR, OPWDD, and other adult service agencies"]),
        ("What to check before your child exits", ["Is every section complete and accurate?", "Does it reflect your child's actual strengths and needs?", "Are the recommendations specific and actionable?", "Does your child have a copy to keep?", "Has the school connected your child to any adult service agencies?"]),
    ]

    for title, items in exit_items:
        st.markdown(f"**{title}:**")
        for item in items:
            st.markdown(f'<div style="background:#F8FAFF;border-radius:6px;padding:7px 12px;margin-bottom:5px;font-size:0.86rem;color:#334155;">• {item}</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)

with tab_rights:
    st.markdown("### Transition Rights Every Parent Should Know")
    rights = [
        ("Transition planning must start by age 15", "The IEP must include transition goals and services starting at the IEP in effect when the student turns 15. NYC DOE recommends starting at 14.", "Critical"),
        ("The student must be invited to transition meetings", "Once transition is being planned, the student must be invited to participate in IEP meetings. Their goals and preferences must be documented.", "Required"),
        ("Services must be based on the student's strengths and interests", "Transition services cannot be generic. They must be based on age-appropriate assessments of the student's interests, preferences, and needs.", "Required"),
        ("Agency representatives must be invited when appropriate", "If transition services will be provided by an outside agency (like ACCES-VR), that agency must be invited to the IEP meeting.", "Required"),
        ("Students stay in school until age 21", "Students with disabilities have the right to a free appropriate public education until they graduate with a diploma OR turn 21, whichever comes first.", "Critical"),
        ("You can request an independent transition assessment", "If you disagree with the school's transition assessment or planning, you can request an independent evaluation at the school's expense.", "Your right"),
        ("Transfer of rights at age 18", "In New York, at age 18 most rights transfer from the parent to the student. The school must notify both parent and student of this transfer one year before the student's 18th birthday.", "Important"),
    ]
    for right, desc, tag in rights:
        tag_colors = {"Critical": ("#FEE2E2","#C62828"), "Required": ("#D1FAE5","#065F46"), "Your right": ("#EFF6FF","#1E40AF"), "Important": ("#FEF3C7","#D97706")}
        bg, fg = tag_colors.get(tag, ("#F3F4F6","#374151"))
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:9px;
                    padding:12px 16px;margin-bottom:8px;display:flex;gap:10px;align-items:flex-start;">
            <span style="background:{bg};color:{fg};border-radius:5px;padding:2px 8px;
                         font-size:0.7rem;font-weight:700;white-space:nowrap;margin-top:2px;">{tag}</span>
            <div>
                <div style="font-weight:700;color:#1E293B;font-size:0.88rem;margin-bottom:3px;">{right}</div>
                <div style="color:#64748B;font-size:0.84rem;line-height:1.6;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.get("pdf_loaded"):
        st.markdown("---")
        with st.expander("What your document says about transition"):
            results = search_chunks([], "transition postsecondary goals services age", top_k=3)
            for r in results:
                st.markdown(f"""
                <div style="background:#F8FAFF;border-left:3px solid #16A34A;
                            border-radius:6px;padding:10px 14px;margin-bottom:8px;
                            font-size:0.85rem;color:#334155;line-height:1.75;">
                    <b>Page {r['page']} · {r['section']}</b><br>{r['text'][:350]}…
                </div>""", unsafe_allow_html=True)
