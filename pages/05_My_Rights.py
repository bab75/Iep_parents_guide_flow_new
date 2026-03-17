"""
Page: My Rights
Every parent right extracted from the uploaded PDF. Plain English. What to say. What to do.
"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="My Rights · IEP Guide", page_icon="🛡️", layout="wide")

from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner, answer_card

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

page_header("🛡️", "My Rights as a Parent",
            "Every right you have in the IEP process — pulled from your document — with what to say and what to do",
            "#DC2626")
status_banner()

# ── Rights definitions (always available — federal IDEA baseline) ─────────────
RIGHTS = [
    {
        "title":   "Right to Request an Evaluation",
        "summary": "You can ask for a special education evaluation at any time, in writing. The school cannot ignore a written request. You do not need a reason beyond believing your child may have a disability.",
        "what_to_say": '"I am writing to request a comprehensive special education evaluation for my child [name]. I believe they may have a disability affecting their education."',
        "if_refused": "The school must give you written Prior Written Notice explaining why they are refusing. You can then request mediation or file a complaint with the state.",
        "query": "referral request evaluation parent right",
        "law": "IDEA § 300.301",
        "icon": "✉️",
    },
    {
        "title":   "Right to Give or Withhold Consent",
        "summary": "Nothing happens without your written agreement. No evaluation. No placement. You can say yes to some parts and no to others. You can also take back your consent later.",
        "what_to_say": '"I consent to the psychological and educational evaluation but not the speech evaluation at this time."',
        "if_refused": "If the school proceeds without consent, that is an IDEA violation. Document it in writing and contact the CSE supervisor.",
        "query": "parental consent written required evaluation placement",
        "law": "IDEA § 300.300",
        "icon": "✍️",
    },
    {
        "title":   "Right to Participate in the IEP Meeting",
        "summary": "You are a full, equal member of the IEP team. The school cannot finalize an IEP without making reasonable efforts to include you. You can bring a support person.",
        "what_to_say": '"I want to bring [name — advocate, relative, friend] to support me at the IEP meeting. Is that okay?"',
        "if_refused": "The school must reschedule if you cannot attend at the proposed time. They cannot hold the meeting and finalize the IEP without you unless they have documented repeated failed attempts to include you.",
        "query": "parent IEP team member meeting participation",
        "law": "IDEA § 300.321",
        "icon": "🤝",
    },
    {
        "title":   "Right to Prior Written Notice",
        "summary": "Before the school changes, proposes, or refuses anything about your child's evaluation, placement, or services, they must give you written notice explaining exactly why.",
        "what_to_say": '"I have not received Prior Written Notice about this change. Please provide it in writing before moving forward."',
        "if_refused": "Moving forward without PWN is a procedural violation. Document it. Include this in any complaint you file.",
        "query": "prior written notice PWN proposed refused action",
        "law": "IDEA § 300.503",
        "icon": "📝",
    },
    {
        "title":   "Right to Procedural Safeguards Notice",
        "summary": "You must receive a copy of your full rights (called Procedural Safeguards) at least once per year, and at key moments including the initial referral.",
        "what_to_say": '"I have not received the Procedural Safeguards notice. Please provide me a copy today."',
        "if_refused": "Not providing Procedural Safeguards is a violation. Request it in writing and note the date it was not provided.",
        "query": "procedural safeguards notice parent rights annual",
        "law": "IDEA § 300.504",
        "icon": "📋",
    },
    {
        "title":   "Right to Access School Records",
        "summary": "You can request copies of all your child's school records — evaluations, IEPs, progress reports, meeting notes — at any time. Schools must provide them within 45 days at no cost.",
        "what_to_say": '"I am requesting copies of all educational records for my child [name], including all evaluation reports, IEPs, and meeting notes."',
        "if_refused": "This is a federal right under FERPA as well as IDEA. If refused, file a complaint with the school district and the state education department.",
        "query": "educational records access parent copy request",
        "law": "IDEA § 300.613 / FERPA",
        "icon": "📂",
    },
    {
        "title":   "Right to an Independent Educational Evaluation (IEE)",
        "summary": "If you disagree with the school's evaluation, you can ask for an evaluation done by an independent evaluator at the school's expense. The school must either pay for it or file for a due process hearing to defend their evaluation.",
        "what_to_say": "\"I disagree with the school's evaluation. I am requesting an Independent Educational Evaluation at public expense.\"",
        "if_refused": "The school must either pay for the IEE or immediately file for a due process hearing. They cannot simply deny the request.",
        "query": "independent educational evaluation IEE public expense disagree",
        "law": "IDEA § 300.502",
        "icon": "🔬",
    },
    {
        "title":   "Right to Disagree and Request Mediation",
        "summary": "You can disagree with any part of the IEP, evaluation, or placement and request free mediation. A neutral third party helps both sides reach an agreement. This does not give up your other rights.",
        "what_to_say": '"I disagree with [specific part of IEP/placement]. I would like to request mediation to resolve this disagreement."',
        "if_refused": "The school cannot refuse mediation when you request it. It is a free federal right. Contact the state education department if refused.",
        "query": "mediation dispute resolution disagree IEP",
        "law": "IDEA § 300.506",
        "icon": "⚖️",
    },
    {
        "title":   "Right to File a State Complaint",
        "summary": "If you believe the school violated IDEA, you can file a free complaint with the state education department. The state must investigate within 60 days.",
        "what_to_say": "Write to the state education department's special education office: 'I am filing a complaint regarding [specific violation] at [school name] on [date].'",
        "if_refused": "State complaints go to the state department directly — you do not need school permission.",
        "query": "state complaint IDEA violation file",
        "law": "IDEA § 300.151",
        "icon": "📬",
    },
    {
        "title":   "Stay Put Right — Services Continue During Disputes",
        "summary": "While any dispute is being resolved, your child has the right to stay in their current placement and continue receiving their current services. The school cannot move or remove your child during a disagreement.",
        "what_to_say": '"While this dispute is being resolved, I expect my child to remain in their current placement and receive all services in the current IEP under Stay Put."',
        "if_refused": "Contact the state education department immediately. Violating Stay Put is a serious IDEA violation.",
        "query": "stay put pendency current placement services dispute",
        "law": "IDEA § 300.518",
        "icon": "🛑",
    },
    {
        "title":   "Right to Translation and Interpretation",
        "summary": "All IEP meetings and documents must be available in your preferred language. The school must provide a qualified interpreter — not a student or unqualified staff member.",
        "what_to_say": '"I need an interpreter for [language] at the IEP meeting. Please arrange one."',
        "if_refused": "Denying language access is a civil rights violation in addition to an IDEA violation. Contact the Office of Civil Rights if refused.",
        "query": "translation interpretation language parent preferred",
        "law": "IDEA § 300.322(e)",
        "icon": "🌐",
    },
]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_rights, tab_fromPDF, tab_scripts = st.tabs([
    "All My Rights", "What Your Document Says", "What to Say Scripts"
])

# ── TAB 1: All Rights ─────────────────────────────────────────────────────────
with tab_rights:
    st.markdown("""
    <div style="background:#FFF1F2;border:1px solid #FCA5A5;border-radius:10px;
                padding:12px 18px;margin-bottom:18px;font-size:0.88rem;color:#9F1239;">
        <strong>Remember:</strong> These rights are guaranteed by federal law (IDEA).
        They apply in every state. Schools cannot take them away.
        You never have to sign an IEP at the meeting — take it home and review it first.
    </div>
    """, unsafe_allow_html=True)

    for right in RIGHTS:
        with st.expander(f"{right['icon']}  {right['title']}  ·  {right['law']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div style="background:#FFF1F2;border-radius:10px;padding:14px;margin-bottom:8px;">
                    <div style="font-weight:700;color:#DC2626;font-size:0.82rem;
                                margin-bottom:6px;">What this right means</div>
                    <div style="color:#374151;font-size:0.88rem;line-height:1.75;">
                        {right['summary']}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:#FEF2F2;border-radius:10px;padding:14px;">
                    <div style="font-weight:700;color:#DC2626;font-size:0.82rem;
                                margin-bottom:6px;">If the school refuses</div>
                    <div style="color:#374151;font-size:0.88rem;line-height:1.75;">
                        {right['if_refused']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="background:#F0FDF4;border-radius:10px;padding:14px;margin-bottom:8px;">
                    <div style="font-weight:700;color:#16A34A;font-size:0.82rem;
                                margin-bottom:6px;">What to say</div>
                    <div style="color:#374151;font-size:0.88rem;line-height:1.75;
                                font-style:italic;">
                        {right['what_to_say']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.pdf_loaded:
                    if st.button(f"Find in my document", key=f"find_{right['title'][:15]}",
                                 use_container_width=True):
                        results = search_chunks(
                            [], right["query"], top_k=2
                        )
                        st.session_state[f"right_result_{right['title'][:15]}"] = results

                    cached = st.session_state.get(f"right_result_{right['title'][:15]}", [])
                    if cached:
                        for r in cached:
                            st.markdown(f"""
                            <div style="background:#EFF6FF;border-left:3px solid #2563EB;
                                        border-radius:6px;padding:10px 12px;margin-top:6px;
                                        font-size:0.82rem;line-height:1.7;color:#1E3A8A;">
                                📄 Page {r['page']}: {r['text'][:250]}…
                            </div>
                            """, unsafe_allow_html=True)

# ── TAB 2: From PDF ───────────────────────────────────────────────────────────
with tab_fromPDF:
    if not st.session_state.pdf_loaded:
        st.info("Upload your PDF on the Home page to see what your specific document says about parent rights.")
    else:
        st.markdown("""
        <div style="font-size:0.88rem;color:#64748B;margin-bottom:14px;">
            These passages are taken directly from your uploaded document.
        </div>
        """, unsafe_allow_html=True)
        rights_query = "parent rights procedural safeguards consent notice dispute"
        results = search_chunks([], rights_query, top_k=6)
        if results:
            for i, r in enumerate(results, 1):
                answer_card(r, "parent rights", i)
        else:
            st.info("No parent rights passages found. Try the Ask Questions page and search for 'parent rights'.")

# ── TAB 3: Scripts ────────────────────────────────────────────────────────────
with tab_scripts:
    st.markdown("""
    <div style="font-size:0.88rem;color:#64748B;margin-bottom:16px;">
        Copy these scripts to use at IEP meetings or in written communications.
    </div>
    """, unsafe_allow_html=True)

    scripts = [
        ("Before agreeing to anything at a meeting",
         "I would like to take the IEP home to review it before signing. I understand I have the right to do this and I will respond within [X] days."),
        ("When asking for your rights notice",
         "I have not yet received a copy of the Procedural Safeguards notice. I am requesting that you provide one today, as required by IDEA."),
        ("When disagreeing with an evaluation",
         "I disagree with the evaluation conducted by the school. I am formally requesting an Independent Educational Evaluation (IEE) at public expense, as is my right under IDEA § 300.502."),
        ("When requesting mediation",
         "I disagree with [specific item in IEP/placement decision]. I am requesting free mediation through the state to resolve this disagreement."),
        ("When the school misses the 60-day deadline",
         "My written consent was signed on [date]. The 60 school-day deadline for completing the evaluation and holding an IEP meeting was [deadline date]. That date has passed without a meeting. I am formally requesting an immediate IEP meeting and reserving the right to file a complaint with the state education department."),
        ("When requesting records",
         "I am formally requesting copies of all educational records for my child [name], including all evaluation reports, IEPs, progress notes, and meeting minutes. I understand these must be provided within 45 days at no cost to me."),
    ]

    for situation, script in scripts:
        st.markdown(f"""
        <div style="background:white;border:1px solid #E2E8F0;border-radius:10px;
                    padding:16px 18px;margin-bottom:10px;">
            <div style="font-family:'Nunito',sans-serif;font-weight:800;
                        color:#1E293B;font-size:0.88rem;margin-bottom:8px;">
                {situation}</div>
            <div style="background:#F8FAFF;border-left:3px solid #2563EB;
                        border-radius:6px;padding:12px 14px;
                        font-size:0.88rem;line-height:1.75;color:#1E40AF;
                        font-style:italic;">
                "{script}"</div>
        </div>
        """, unsafe_allow_html=True)
