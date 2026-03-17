"""
Page: IEP Meeting Prep
Checklist-style guide for before, during, and after the IEP meeting.
Pulled from SOPM pages 38-50.
"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Meeting Prep · IEP Guide", page_icon="📋", layout="wide")
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner
from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
apply_theme(); init_session(); sidebar_brand(); auto_load_from_docs()
page_header("📋", "IEP Meeting Preparation", "Everything you need to do before, during and after the IEP meeting — so you are never caught off guard", "#0D9488")
status_banner()

tab_before, tab_who, tab_during, tab_after, tab_scripts = st.tabs([
    "Before the Meeting", "Who Must Be There", "During the Meeting", "After the Meeting", "Scripts to Use"
])

with tab_before:
    st.markdown("### What to Do Before Your IEP Meeting")
    st.info("The school must give you reasonable notice before the meeting. Use that time to prepare. You are an equal member of the team — arriving prepared makes a difference.")

    steps = [
        ("Request documents in advance", "You have the right to see all evaluation reports, progress notes, and the draft IEP before the meeting. Send a written request at least one week early.", "Required by IDEA"),
        ("Review your child's current IEP", "Read the current goals. Which ones were met? Which weren't? Note anything that seems wrong or incomplete.", "Preparation"),
        ("Write down your observations", "You know your child better than anyone. Write down: what is going well, what is still hard, what you see at home. Bring this to the meeting.", "Your right"),
        ("Talk to your child's teachers", "Contact the general education teacher and any service providers for informal updates before the formal meeting.", "Best practice"),
        ("Bring someone you trust", "You can bring a friend, family member, advocate, or disability specialist to support you. Notify the school in advance.", "Your right"),
        ("Write your questions down", "Use the questions from the Glossary and Rights pages. Having them written means you won't forget in the moment.", "Preparation"),
        ("Confirm the meeting location and who will attend", "Ask who from the school will be at the meeting. Make sure all required members will be present.", "Required"),
        ("Know you don't have to sign anything that day", "You are never required to sign the IEP at the meeting. You can take it home and review it first.", "Critical right"),
    ]

    for step, desc, tag in steps:
        tag_colors = {"Required by IDEA": ("#DBEAFE","#1E40AF"), "Critical right": ("#FEE2E2","#C62828"), "Your right": ("#D1FAE5","#065F46"), "Preparation": ("#F3F4F6","#374151"), "Best practice": ("#FEF3C7","#92400E")}
        bg, fg = tag_colors.get(tag, ("#F3F4F6","#374151"))
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;
                    padding:14px 18px;margin-bottom:8px;display:flex;gap:14px;align-items:flex-start;">
            <div style="width:10px;height:10px;border-radius:50%;background:#0D9488;
                        flex-shrink:0;margin-top:6px;"></div>
            <div style="flex:1;">
                <div style="font-weight:700;color:#1E293B;font-size:0.9rem;margin-bottom:3px;">{step}</div>
                <div style="color:#64748B;font-size:0.85rem;line-height:1.65;">{desc}</div>
            </div>
            <span style="background:{bg};color:{fg};border-radius:6px;padding:2px 10px;
                         font-size:0.72rem;font-weight:700;white-space:nowrap;">{tag}</span>
        </div>
        """, unsafe_allow_html=True)

with tab_who:
    st.markdown("### Who Must Be at the IEP Meeting")
    st.info("IDEA lists required IEP team members. The meeting cannot finalize an IEP without making reasonable efforts to include all required members. Absent members must be excused in writing.")

    members = [
        ("You — the Parent", "Required", "#DC2626", "You are a full, equal member. The school cannot hold the meeting and finalize the IEP without making reasonable efforts to include you. If you cannot attend at the proposed time, they must reschedule."),
        ("General Education Teacher", "Required", "#2563EB", "Must attend if your child is — or may be — in a general education classroom. Provides insight into grade-level expectations and classroom performance."),
        ("Special Education Teacher or Related Service Provider", "Required", "#7C3AED", "The special ed teacher or, if only related services are being provided, a related service provider. Knows your child's IEP goals and current performance."),
        ("District Representative (CSE Chairperson)", "Required", "#D97706", "A school official who is qualified to provide or supervise special education, knows the curriculum, and has authority to commit district resources. Cannot be excused without your written consent."),
        ("Person to Interpret Evaluation Results", "Required when evaluations discussed", "#16A34A", "Someone who can explain what the evaluation scores mean in plain language. Often the school psychologist. Required at any meeting where evaluations are discussed."),
        ("School Psychologist", "Required for initial evaluations and certain reviews", "#0891B2", "Required when initial eligibility is being determined or when a new psychological assessment is being reviewed."),
        ("Your Child", "Required when appropriate — typically age 14+", "#E65100", "For transition planning meetings, the student should attend when appropriate. Their preferences and goals are part of transition planning."),
        ("Other Professionals (at parent or school request)", "Optional — invited as needed", "#475569", "Any person with knowledge or expertise about your child — a private therapist, pediatrician, advocate, or outside evaluator — can be invited by you or the school."),
    ]

    for name, status, color, desc in members:
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-left:5px solid {color};
                    border-radius:10px;padding:14px 18px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;
                        flex-wrap:wrap;gap:6px;margin-bottom:6px;">
                <div style="font-weight:800;color:{color};font-size:0.92rem;">{name}</div>
                <span style="background:{color}18;color:{color};border-radius:6px;
                             padding:2px 10px;font-size:0.75rem;font-weight:700;">{status}</span>
            </div>
            <div style="color:#475569;font-size:0.86rem;line-height:1.65;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with tab_during:
    st.markdown("### During the IEP Meeting")
    st.warning("Remember: You do NOT have to sign anything at the meeting. Take notes. Ask for clarification on anything you do not understand.")

    sections_meeting = [
        ("At the start", [
            "Confirm that all required team members are present (or properly excused in writing)",
            "Ask that meeting minutes be kept and that you receive a copy",
            "Ask if an interpreter is available if you need one",
            "Confirm you will receive a copy of the IEP before you leave or shortly after",
        ]),
        ("When reviewing Present Levels", [
            "Ask: Is this based on current data or last year's evaluation?",
            "Share your observations from home — they must be considered",
            "Ask if the description matches what you know about your child",
            "Note any gaps — areas not mentioned that affect your child at school",
        ]),
        ("When reviewing Goals", [
            "Ask: How will we measure this goal?",
            "Ask: What is the baseline — where is my child starting?",
            "Ask: Is this goal realistic for one year AND ambitious enough?",
            "Make sure every goal connects to something in Present Levels",
        ]),
        ("When reviewing Services", [
            "Ask: How many minutes per week will my child receive each service?",
            "Ask: Will services be push-in or pull-out? Why?",
            "Ask: Who specifically will provide this service?",
            "Ask: What happens if the provider is absent?",
        ]),
        ("When reviewing Placement", [
            "Ask: What less restrictive option was considered?",
            "Ask: Why is this the least restrictive appropriate placement?",
            "Ask: Will my child have any time with non-disabled peers?",
            "If you disagree — say so out loud and ask that it be noted in the minutes",
        ]),
    ]

    for section, items in sections_meeting:
        st.markdown(f"""
        <div style="font-family:'Nunito',sans-serif;font-weight:800;color:#0D9488;
                    font-size:0.88rem;text-transform:uppercase;letter-spacing:.05em;
                    margin:16px 0 8px;">{section}</div>
        """, unsafe_allow_html=True)
        for item in items:
            st.markdown(f"""
            <div style="background:#F0FDF4;border-radius:7px;padding:8px 12px;
                        margin-bottom:5px;font-size:0.86rem;color:#166534;
                        border-left:3px solid #16A34A;">✓ {item}</div>
            """, unsafe_allow_html=True)

with tab_after:
    st.markdown("### After the IEP Meeting")

    after_steps = [
        ("Review the IEP carefully before signing", "You do not have to sign at the meeting. Take it home. Read every section. Compare it to what was discussed.", "Critical"),
        ("Request a copy if not provided", "You must receive a copy of the IEP. If not given at the meeting, request one in writing immediately.", "Your right"),
        ("Note your disagreements in writing", "If you disagree with any part of the IEP, write a letter to the CSE noting your specific objections. Keep a copy.", "Important"),
        ("Contact service providers after 2 weeks", "If services haven't started within 2 weeks of the IEP date, contact the school in writing.", "Follow up"),
        ("Request progress reports on schedule", "The IEP must specify how often you will receive progress reports. Hold the school to that schedule.", "Your right"),
        ("Keep all documents organized", "Keep every IEP, evaluation report, and communication in a folder. You may need them for future meetings or disputes.", "Best practice"),
        ("Know your options if you disagree", "If you disagree with the IEP, you have the right to mediation, a state complaint, or a due process hearing. See the Dispute Resolution page.", "Your right"),
    ]

    for step, desc, tag in after_steps:
        tag_colors = {"Critical": ("#FEE2E2","#C62828"), "Your right": ("#D1FAE5","#065F46"), "Important": ("#FEF3C7","#D97706"), "Follow up": ("#EFF6FF","#1E40AF"), "Best practice": ("#F3F4F6","#374151")}
        bg, fg = tag_colors.get(tag, ("#F3F4F6","#374151"))
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:9px;
                    padding:12px 16px;margin-bottom:8px;display:flex;gap:12px;align-items:flex-start;">
            <span style="background:{bg};color:{fg};border-radius:5px;padding:2px 8px;
                         font-size:0.72rem;font-weight:700;white-space:nowrap;margin-top:2px;">{tag}</span>
            <div>
                <div style="font-weight:700;color:#1E293B;font-size:0.88rem;margin-bottom:2px;">{step}</div>
                <div style="color:#64748B;font-size:0.83rem;line-height:1.6;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_scripts:
    st.markdown("### What to Say in the Meeting")
    st.caption("Use these phrases when you need to speak up. You have every right to say these things.")

    scripts = [
        ("To slow down or get clarification", "\"I want to make sure I understand. Can you explain what that means in plain language?\""),
        ("To disagree with a goal", "\"I don't think this goal is ambitious enough for my child. Can we discuss raising the target?\""),
        ("To disagree with placement", "\"I'm concerned about this placement recommendation. What less restrictive option was considered and why was it rejected?\""),
        ("To note your disagreement formally", "\"I disagree with this part of the IEP and I would like that noted in the meeting minutes.\""),
        ("To ask for more time before signing", "\"I'd like to take the IEP home to review it before I sign. I'll respond within the week.\""),
        ("To request services weren't discussed", "\"I'd like to request that we consider adding [service] to the IEP. My reason is [brief explanation].\""),
        ("To ask about your child's progress", "\"Can you show me the actual data from the past year? How much progress was made on each goal?\""),
        ("If you feel rushed", "\"I want to make sure we have enough time for everything. Can we schedule a follow-up meeting if we don't finish today?\""),
        ("To invoke your rights", "\"I'm aware of my rights under IDEA. I'd like a copy of the Procedural Safeguards notice today please.\""),
    ]

    for situation, script in scripts:
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;
                    padding:14px 18px;margin-bottom:10px;">
            <div style="font-weight:700;color:#0D9488;font-size:0.85rem;margin-bottom:8px;">{situation}</div>
            <div style="background:#F0FDFA;border-left:3px solid #0D9488;border-radius:6px;
                        padding:10px 14px;font-size:0.88rem;color:#134E4A;font-style:italic;">
                {script}</div>
        </div>
        """, unsafe_allow_html=True)
