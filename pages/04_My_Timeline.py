"""
Page: My Timeline
Personal 60-day deadline calculator. Enter consent date → see where you are.
"""
import streamlit as st
import sys
from datetime import date, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="My Timeline · IEP Guide", page_icon="⏱️", layout="wide")

from utils.rag_engine import init_session, auto_load_from_docs, search_chunks
from utils.theme import apply_theme, sidebar_brand, page_header, status_banner, answer_card

apply_theme()
init_session()
sidebar_brand()
auto_load_from_docs()

page_header("⏱️", "My Personal IEP Timeline",
            "Enter the date you signed consent — we'll show your deadlines and what should happen next",
            "#D97706")
status_banner()

# ── Timeline milestones (school days from consent) ────────────────────────────
MILESTONES = [
    (0,  "You signed consent to evaluate",
         "The 60-day clock starts today. Keep a copy of the signed consent form.",
         "#2563EB", "green"),
    (5,  "School must acknowledge your referral in writing",
         "You should receive written confirmation that your referral was received.",
         "#0D9488", "blue"),
    (10, "Social History Interview should be scheduled",
         "The school social worker will contact you to schedule an interview to discuss your child's history and explain your rights.",
         "#0D9488", "blue"),
    (15, "Pre-assessment planning complete",
         "The evaluation team should have agreed on what assessments will be conducted and who will conduct them.",
         "#7C3AED", "blue"),
    (30, "Evaluations should be underway",
         "Most or all assessments should be in progress. Follow up if you have not heard from evaluators.",
         "#7C3AED", "blue"),
    (45, "Evaluations should be complete",
         "All assessments should be finished. Reports should be written. You should receive copies before the IEP meeting.",
         "#D97706", "amber"),
    (55, "IEP meeting notice should be sent to you",
         "You must receive written notice of the IEP meeting with enough time to attend. The notice should include date, time, location and who will be there.",
         "#DC2626", "red"),
    (60, "IEP meeting must be held — DEADLINE",
         "This is the legal deadline. The eligibility meeting and IEP meeting must occur by this date. If this passes without a meeting, the school is in violation.",
         "#DC2626", "red"),
]

def add_school_days(start: date, school_days: int) -> date:
    """Add school days (Mon-Fri only) to a date."""
    current = start
    days_added = 0
    while days_added < school_days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Mon-Fri
            days_added += 1
    return current

def school_days_between(start: date, end: date) -> int:
    """Count school days between two dates."""
    count = 0
    current = start
    while current < end:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count += 1
    return count

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-radius:14px;border:1px solid #E2E8F0;
            padding:24px;margin-bottom:20px;">
    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                color:#1E293B;font-size:1rem;margin-bottom:16px;">
        Enter your dates
    </div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    consent_date = st.date_input(
        "Date you signed consent to evaluate",
        value=None,
        help="The date on the consent form you signed. This starts the 60-day clock.",
        format="MM/DD/YYYY",
    )
with c2:
    child_name = st.text_input("Child's first name (optional)", placeholder="e.g. Alex")
with c3:
    school_name = st.text_input("School name (optional)", placeholder="e.g. Lincoln Elementary")

st.markdown("</div>", unsafe_allow_html=True)

if not consent_date:
    st.markdown("""
    <div style="background:#FFF7ED;border:1px solid #FCD34D;border-radius:10px;
                padding:16px 20px;text-align:center;color:#92400E;font-size:0.9rem;">
        ⬆️ Enter the date you signed the consent form above to see your personal timeline
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Calculate timeline ────────────────────────────────────────────────────────
today        = date.today()
deadline     = add_school_days(consent_date, 60)
days_elapsed = school_days_between(consent_date, today) if today > consent_date else 0
days_left    = max(0, school_days_between(today, deadline))
pct          = min(100, int(days_elapsed / 60 * 100))
is_overdue   = today > deadline
name_str     = f"{child_name}'s" if child_name else "Your child's"

# ── Status banner ─────────────────────────────────────────────────────────────
if is_overdue:
    st.markdown(f"""
    <div style="background:#FEF2F2;border:2px solid #FCA5A5;border-radius:12px;
                padding:18px 24px;margin-bottom:20px;">
        <div style="font-family:'Nunito',sans-serif;font-weight:900;
                    color:#DC2626;font-size:1.1rem;margin-bottom:6px;">
            ⚠️ The 60-day deadline has passed
        </div>
        <div style="color:#7F1D1D;font-size:0.9rem;line-height:1.7;">
            {name_str} IEP meeting was due by <strong>{deadline.strftime('%B %d, %Y')}</strong>.
            Today is {today.strftime('%B %d, %Y')} — {school_days_between(deadline, today)} school days overdue.
            <strong>Write a letter to the CSE supervisor requesting an immediate meeting.</strong>
            You may also file a complaint with your state education department.
        </div>
    </div>
    """, unsafe_allow_html=True)
elif days_left <= 5:
    st.markdown(f"""
    <div style="background:#FFF7ED;border:2px solid #FCD34D;border-radius:12px;
                padding:18px 24px;margin-bottom:20px;">
        <div style="font-family:'Nunito',sans-serif;font-weight:900;
                    color:#D97706;font-size:1.1rem;margin-bottom:6px;">
            ⏰ Deadline is very soon — {days_left} school days left
        </div>
        <div style="color:#92400E;font-size:0.9rem;line-height:1.7;">
            The IEP meeting must happen by <strong>{deadline.strftime('%B %d, %Y')}</strong>.
            Contact the school immediately if you have not received a meeting notice.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;
                padding:18px 24px;margin-bottom:20px;">
        <div style="font-family:'Nunito',sans-serif;font-weight:900;
                    color:#15803D;font-size:1.1rem;margin-bottom:6px;">
            ✅ On track — {days_left} school days until the deadline
        </div>
        <div style="color:#166534;font-size:0.9rem;">
            {name_str} IEP meeting must happen by <strong>{deadline.strftime('%B %d, %Y')}</strong>.
            You are on day {days_elapsed} of 60.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Progress bar ──────────────────────────────────────────────────────────────
bar_color = "#DC2626" if is_overdue else ("#D97706" if pct >= 80 else "#16A34A")
st.markdown(f"""
<div style="background:white;border-radius:12px;border:1px solid #E2E8F0;
            padding:16px 20px;margin-bottom:20px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
        <span style="font-weight:700;color:#1E293B;font-size:0.88rem;">
            Day {days_elapsed} of 60</span>
        <span style="font-weight:700;color:{bar_color};font-size:0.88rem;">
            {pct}% of timeline used</span>
    </div>
    <div style="background:#F1F5F9;border-radius:8px;height:12px;overflow:hidden;">
        <div style="background:{bar_color};height:100%;width:{min(pct,100)}%;
                    border-radius:8px;transition:width 0.5s;"></div>
    </div>
    <div style="display:flex;justify-content:space-between;margin-top:6px;
                font-size:0.75rem;color:#94A3B8;">
        <span>Consent signed: {consent_date.strftime('%b %d, %Y')}</span>
        <span>Today: {today.strftime('%b %d, %Y')}</span>
        <span>Deadline: {deadline.strftime('%b %d, %Y')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Key dates grid ────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Nunito',sans-serif;font-weight:800;
            color:#1E293B;font-size:1rem;margin-bottom:12px;">
    Your Key Dates
</div>
""", unsafe_allow_html=True)

m_cols = st.columns(4)
key_dates = [
    ("Consent signed",    consent_date,                    "#2563EB"),
    ("~Evaluations due",  add_school_days(consent_date,45),"#7C3AED"),
    ("~Meeting notice",   add_school_days(consent_date,55),"#D97706"),
    ("IEP deadline",      deadline,                        "#DC2626"),
]
for col, (label, dt, color) in zip(m_cols, key_dates):
    passed = today > dt
    with col:
        st.markdown(f"""
        <div style="background:{'#F0FDF4' if passed else 'white'};
                    border:1px solid {color}40;border-top:3px solid {color};
                    border-radius:10px;padding:14px;text-align:center;">
            <div style="font-size:0.72rem;font-weight:700;color:{color};
                        text-transform:uppercase;letter-spacing:0.04em;
                        margin-bottom:4px;">{label}</div>
            <div style="font-family:'Nunito',sans-serif;font-weight:800;
                        color:#1E293B;font-size:0.95rem;">
                {dt.strftime('%b %d')}</div>
            <div style="font-size:0.72rem;color:#94A3B8;margin-top:2px;">
                {dt.strftime('%Y')}</div>
            {'<div style="font-size:0.72rem;color:#16A34A;font-weight:700;margin-top:4px;">✓ Passed</div>' if passed else ''}
        </div>
        """, unsafe_allow_html=True)

# ── Milestone timeline ────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Nunito',sans-serif;font-weight:800;
            color:#1E293B;font-size:1rem;margin:20px 0 12px;">
    Milestone Checklist
</div>
""", unsafe_allow_html=True)

for school_day, title, description, color, status_type in MILESTONES:
    milestone_date  = add_school_days(consent_date, school_day)
    has_passed      = today >= milestone_date
    is_next         = not has_passed and school_days_between(today, milestone_date) <= 7
    is_deadline     = school_day == 60

    if has_passed:
        icon, bg, border = "✅", "#F0FDF4", "#86EFAC"
    elif is_next:
        icon, bg, border = "⏰", "#FFF7ED", "#FCD34D"
    elif is_deadline:
        icon, bg, border = "🔴", "#FEF2F2", "#FCA5A5"
    else:
        icon, bg, border = "⬜", "white", "#E2E8F0"

    days_away = school_days_between(today, milestone_date) if not has_passed else 0
    timing_str = (f"{days_away} school days away" if not has_passed and days_away > 0
                  else ("Today" if milestone_date == today else "Passed"))

    st.markdown(f"""
    <div style="background:{bg};border:1px solid {border};border-radius:10px;
                padding:14px 18px;margin-bottom:8px;
                display:flex;gap:14px;align-items:flex-start;">
        <div style="font-size:1.3rem;flex-shrink:0;margin-top:2px;">{icon}</div>
        <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;flex-wrap:wrap;gap:4px;margin-bottom:4px;">
                <div style="font-family:'Nunito',sans-serif;font-weight:800;
                            color:#1E293B;font-size:0.9rem;">
                    Day {school_day}: {title}</div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <span style="background:{color}15;color:{color};border-radius:6px;
                                 padding:2px 9px;font-size:0.72rem;font-weight:700;">
                        {milestone_date.strftime('%b %d, %Y')}</span>
                    <span style="background:#F1F5F9;color:#475569;border-radius:6px;
                                 padding:2px 9px;font-size:0.72rem;font-weight:600;">
                        {timing_str}</span>
                </div>
            </div>
            <div style="color:#475569;font-size:0.85rem;line-height:1.65;">
                {description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── What to do if deadline passes ─────────────────────────────────────────────
if is_overdue and st.session_state.pdf_loaded:
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Nunito',sans-serif;font-weight:800;
                color:#DC2626;font-size:1rem;margin-bottom:10px;">
        What your document says to do when deadlines are missed:
    </div>
    """, unsafe_allow_html=True)
    results = search_chunks(
        [],
        "timeline violation complaint due process parent rights",
        top_k=2
    )
    for i, r in enumerate(results, 1):
        answer_card(r, "timeline violation", i)

# ── Export ────────────────────────────────────────────────────────────────────
st.markdown("---")
export_text = f"""IEP TIMELINE SUMMARY
{name_str} IEP Timeline
{'School: ' + school_name if school_name else ''}

Consent Signed:   {consent_date.strftime('%B %d, %Y')}
Today:            {today.strftime('%B %d, %Y')}
60-Day Deadline:  {deadline.strftime('%B %d, %Y')}
Days Elapsed:     {days_elapsed} of 60 school days
Days Remaining:   {days_left} school days
Status:           {'OVERDUE' if is_overdue else 'On Track'}

KEY MILESTONES:
"""
for sd, title, _, _, _ in MILESTONES:
    md = add_school_days(consent_date, sd)
    export_text += f"Day {sd:2d} ({md.strftime('%b %d, %Y')}): {title}\n"

st.download_button(
    "⬇️ Save My Timeline",
    export_text,
    file_name=f"IEP_Timeline_{consent_date}.txt",
    mime="text/plain",
)
