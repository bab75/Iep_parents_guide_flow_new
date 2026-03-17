"""
IEP Parent App — RAG Engine (v2)
Multi-PDF support. All chunks tagged with doc_name.
Plain-English summaries, bullet extraction, action lines — no API needed.
"""

import re
import streamlit as st
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

# ── Question templates ────────────────────────────────────────────────────────
QUESTION_TEMPLATES = [
    (r"referral",                       "How does the referral process work?"),
    (r"child find",                     "What is Child Find and who does it cover?"),
    (r"consent",                        "When is parental consent required?"),
    (r"evaluat",                        "What happens during the evaluation?"),
    (r"60.day|timeline|timeframe",      "What is the 60-day timeline?"),
    (r"eligib",                         "How is eligibility for special education determined?"),
    (r"classif",                        "What disability classifications are used?"),
    (r"iep meeting|meeting",            "What happens at an IEP meeting?"),
    (r"iep team|team comp",             "Who is on the IEP team?"),
    (r"present level",                  "What are Present Levels of Performance?"),
    (r"annual goal",                    "What are annual goals and how are they written?"),
    (r"service",                        "What special education services are available?"),
    (r"related service",                "What are related services?"),
    (r"placement",                      "How is a placement decided?"),
    (r"least restrict|lre",             "What is Least Restrictive Environment (LRE)?"),
    (r"accommodat",                     "What accommodations can be put in an IEP?"),
    (r"modif",                          "What modifications can be made?"),
    (r"annual review",                  "How often is the IEP reviewed?"),
    (r"reevaluat",                      "When does my child get reevaluated?"),
    (r"amendment",                      "How can an IEP be changed between annual reviews?"),
    (r"prior written|pwn",              "What is Prior Written Notice?"),
    (r"procedural safeguard|parent right","What are my rights as a parent?"),
    (r"independent.*eval|iee",          "Can I get an Independent Educational Evaluation?"),
    (r"mediat",                         "How does mediation work?"),
    (r"complaint|due process",          "What can I do if I disagree with the IEP?"),
    (r"transition",                     "What is transition planning?"),
    (r"extend.*school|esy",             "What is Extended School Year (ESY)?"),
    (r"behavior|bip|fba",               "What is a Behavioral Intervention Plan?"),
    (r"paraprofessional|para",          "When does a student get a paraprofessional?"),
    (r"transport",                      "What transportation services are available?"),
    (r"notif",                          "When must the school notify me?"),
    (r"record",                         "How do I get my child's school records?"),
    (r"surrogate",                      "What is a surrogate parent?"),
    (r"transfer",                       "What happens to the IEP when my child transfers schools?"),
    (r"home instruct",                  "What is home instruction?"),
    (r"interim|pendency",               "What happens to services during a dispute?"),
    (r"discipline|suspend",             "What are the rules around discipline for students with IEPs?"),
    (r"manifestat",                     "What is a Manifestation Determination Review?"),
    (r"social histor",                  "What is a Social History Interview?"),
    (r"assistive tech",                 "What assistive technology support is available?"),
    (r"12.month|summer",                "Can my child receive summer services?"),
    (r"preschool|early",                "Are there special education services for preschool children?"),
]

SECTION_CATEGORIES = {
    "Getting Started":  [r"referral", r"child find", r"overview", r"introduction", r"purpose"],
    "Timelines":        [r"timeline", r"timeframe", r"60.day", r"deadline", r"calendar"],
    "Evaluation":       [r"evaluat", r"assess", r"test", r"social histor", r"psycho"],
    "Eligibility":      [r"eligib", r"classif", r"disability", r"determin"],
    "The IEP Document": [r"iep", r"present level", r"annual goal", r"service", r"accommodat", r"modif"],
    "Placement":        [r"placement", r"least restrict", r"lre", r"continuum", r"program"],
    "Parent Rights":    [r"parent right", r"procedural", r"consent", r"notice", r"pwn", r"record", r"iee"],
    "Meetings":         [r"meeting", r"team", r"committee", r"cse"],
    "Disagreements":    [r"mediat", r"complaint", r"due process", r"dispute", r"appeal", r"hearing"],
    "Special Topics":   [r"transition", r"esy", r"behavior", r"bip", r"fba", r"transport",
                         r"discipline", r"suspend", r"assistive", r"paraprofessional"],
}

# ── Plain-English answer templates ────────────────────────────────────────────
PLAIN_ANSWERS = {
    r"referral":              "A referral is the very first step. You or the school ask in writing for a special education evaluation. You do not need a specific reason — if you think your child may need help, you have the right to ask.",
    r"consent":               "The school must get your written permission before doing anything — before any evaluation and before any placement change. You can say yes to some parts and no to others.",
    r"60.day|timeline":       "Once you sign the consent form, the school has 60 school days to complete all evaluations AND hold the IEP meeting. This is a strict legal deadline.",
    r"eligib":                "After evaluations, the full team — including you — meets to decide if your child qualifies under one of 13 disability categories. You are an equal member of this team.",
    r"evaluat":               "A team of specialists evaluates your child in every area where a disability is suspected. They must use more than one test and cannot rely on a single result to make any decision.",
    r"placement":             "Placement is where and how your child will be educated. The law requires the Least Restrictive Environment — your child must be with non-disabled peers as much as possible.",
    r"least restrict|lre":    "Your child must be educated alongside non-disabled students as much as their needs allow. Putting a child in a more separate setting requires written justification from the team.",
    r"prior written|pwn":     "Before the school changes, proposes, or refuses anything about your child's IEP, they must give you a written notice explaining exactly what they are doing and why.",
    r"parent right|procedural":"You have rights at every step: to be part of every decision, get written notice before any changes, see all school records, and disagree through mediation or a formal complaint.",
    r"annual review":         "The IEP must be reviewed at least once every year. The team checks your child's progress, updates goals, and revises services. You are invited and your input matters.",
    r"reevaluat":             "Every 3 years the school does a full reevaluation to check whether your child still qualifies and what their current needs are. You can also request one earlier.",
    r"mediat":                "Mediation is a free, voluntary process where a neutral person helps you and the school reach an agreement. It is faster and less stressful than a formal hearing.",
    r"iep meeting":           "The IEP meeting is where the team writes or reviews your child's education plan. You are a required member. The meeting cannot finalize the plan without reasonable efforts to include you.",
    r"transition":            "For students aged 15 and older, the IEP must include measurable goals for life after school — college, employment, or independent living — and services to reach those goals.",
    r"service":               "Special education services are specialized instruction designed for your child's unique needs. The IEP must specify the type, frequency, duration, and setting for each service.",
    r"related service":       "Related services like speech therapy, occupational therapy, physical therapy, and counseling support your child in benefiting from their main special education program.",
    r"complaint|due process": "If you disagree with any IEP decision, you have three options: free mediation, a state complaint filed with the education department, or a formal due process hearing.",
    r"record":                "You have the right to inspect and get copies of all your child's school records — evaluations, IEPs, progress reports — within 45 days, at no cost to you.",
    r"annual goal":           "Annual goals are specific, measurable targets your child should reach within one year. A proper goal has a starting point, a target, and a clear way to measure progress.",
    r"iee":                   "If you disagree with the school's evaluation, you can request an Independent Educational Evaluation done by someone outside the school, paid for by the school district.",
    r"behavior|bip":          "A Behavioral Intervention Plan uses positive strategies to address challenging behaviors. It must be based on a Functional Behavioral Assessment (FBA) completed first.",
    r"esy":                   "Extended School Year provides services during summer or school breaks for students who would lose significant skills without year-round support.",
    r"social histor":         "A Social History Interview is a meeting with the school social worker where your child's background is discussed and your rights as a parent are explained.",
    r"discipline|suspend":    "Students with IEPs have special discipline protections. Schools must determine if a behavior is related to the disability before making long-term discipline decisions.",
}

ACTION_LINES = {
    r"referral":              "Write a dated letter to the school or CSE office requesting an evaluation. Keep a copy — the date you submit it starts the official process.",
    r"consent":               "Read the consent form carefully before signing. You can ask questions first. You are not required to sign the same day it is given to you.",
    r"60.day|timeline":       "Note the exact date you signed consent. Count 60 school days forward — that is the legal deadline for the IEP meeting to happen.",
    r"eligib":                "Bring your own information, reports, or outside evaluations to the eligibility meeting. Your input must be considered by the team.",
    r"evaluat":               "Ask for copies of all evaluation reports at least a few days before the meeting so you have time to review them carefully.",
    r"placement":             "Ask the team: What less restrictive option was considered, and why was it rejected? They must document this answer.",
    r"prior written|pwn":     "If the school proposes any change, request Prior Written Notice in writing before agreeing. Do not accept verbal explanations alone.",
    r"parent right|procedural":"Ask for a copy of the Procedural Safeguards notice at every meeting. It lists all your legal rights and how to use them.",
    r"annual review":         "Before the annual review, request your child's progress reports so you can review them ahead of time and come prepared.",
    r"mediat":                "Mediation is free and does not give up your other legal rights. It is often a good first step before filing a formal complaint.",
    r"record":                "Send a written request for records by email or letter and keep a copy. Schools must respond within 45 days.",
    r"complaint|due process": "Document every communication with the school in writing. This documentation is essential if you need to file a formal complaint.",
    r"iee":                   "Send a written request for an IEE to the school. They must either agree to pay for it or immediately file for a hearing to defend their evaluation.",
    r"transition":            "If your child is 14 or 15, raise transition planning at the next IEP meeting even if the school has not brought it up — it is legally required.",
    r"annual goal":           "Review each goal in the IEP and ask: How will we know if this goal is met? Who is measuring it, and how often will I get updates?",
    r"social histor":         "The Social History Interview is your first opportunity to share important information about your child. Prepare notes beforehand.",
    r"discipline|suspend":    "If the school wants to suspend or remove your child for more than 10 days, request a Manifestation Determination Review meeting immediately.",
}

# ── Domain weights for scoring ────────────────────────────────────────────────
IEP_DOMAIN_WEIGHTS = {
    "iep": 4, "evaluation": 3, "eligibility": 3, "placement": 3,
    "annual review": 4, "amendment": 2, "consent": 3, "disability": 2,
    "services": 2, "least restrictive": 4, "lre": 4, "transition": 2,
    "prior written notice": 4, "pwn": 4, "parent": 2, "goals": 2,
    "present levels": 3, "fape": 4, "idea": 3, "referral": 3,
    "60 day": 4, "reevaluation": 3, "procedural": 3, "mediation": 3,
    "due process": 4, "discipline": 2, "bip": 3, "fba": 3,
}


# ── PDF extraction ────────────────────────────────────────────────────────────

def extract_pdf(file_obj) -> dict:
    pages = {}
    try:
        data = file_obj.read() if hasattr(file_obj, "read") else open(file_obj, "rb").read()
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return {}
    try:
        import pdfplumber, io
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                pages[i] = (page.extract_text() or "").strip()
        if any(pages.values()):
            return pages
    except Exception:
        pass
    try:
        import fitz, io
        doc = fitz.open(stream=data, filetype="pdf")
        for i, page in enumerate(doc, 1):
            pages[i] = page.get_text().strip()
        return pages
    except Exception as e:
        st.error(f"PDF extraction failed. Install pdfplumber or PyMuPDF. Error: {e}")
        return {}


def detect_sections(pages: dict) -> list:
    """
    Section detector tuned for NYC DOE SOPM PDF format.
    Strategy:
      1. Extract the Table of Contents (pages 2-5) to build a lookup set.
      2. Scan every body page for lines that exactly match a TOC entry.
      3. Fallback: ALL CAPS lines and short isolated lines with ratio >= 4.0.
    """
    import re as _re
    from collections import defaultdict

    # ── Step 1: build TOC lookup from early pages ─────────────────────────
    toc_entries: set = set()
    SKIP_TOC = _re.compile(
        r"^Table of Contents"
        r"|^click on"
        r"|\d+\s*\|\s*NYC DOE"
        r"|^(As of |Last Updated|check this page)"
    )
    for pg in range(1, min(6, max(pages.keys()) + 1)):
        for line in pages.get(pg, "").split("\n"):
            s = line.strip()
            if not s or len(s) < 6 or len(s) > 85:
                continue
            if SKIP_TOC.search(s):
                continue
            alpha = sum(c.isalpha() for c in s) / len(s)
            if alpha < 0.70:
                continue
            toc_entries.add(s.lower().strip())

    # ── Step 2: scan body pages for TOC matches ───────────────────────────
    headings  = []
    seen      = set()
    SKIP_BODY = _re.compile(
        r"^Table of Contents"
        r"|^\d+\s*\|\s*NYC DOE"
        r"|^(As of |Last Updated|check this page)"
        r"|^\d+$"
        r"|^[•\-\*]"
    )

    for page_num in sorted(pages.keys()):
        if page_num <= 5:
            continue   # skip TOC pages themselves
        lines = pages[page_num].split("\n")
        n     = len(lines)

        for i, raw in enumerate(lines):
            s  = raw.strip()
            if not s or len(s) < 5 or len(s) > 85:
                continue
            if SKIP_BODY.search(s):
                continue

            sl    = s.lower().strip()
            conf  = 0

            # Priority 1: exact TOC match
            if sl in toc_entries:
                conf = 90

            # Priority 2: ALL CAPS (e.g. RECOMMENDED SPECIAL EDUCATION...)
            elif s.isupper() and len(s) >= 6:
                conf = 80

            # Priority 3: short line with high surrounding ratio
            elif 8 <= len(s) <= 60:
                bad_ends = ('.', ',', ';', ')', ':', 'and', 'or', 'the')
                is_clean = (
                    s[0].isupper()
                    and not any(s.endswith(e) for e in bad_ends)
                    and len(s.split()) >= 2
                )
                if is_clean:
                    prev_lens = [len(lines[j].strip()) for j in range(max(0,i-2),i)
                                 if lines[j].strip()]
                    next_lens = [len(lines[j].strip()) for j in range(i+1,min(n,i+3))
                                 if lines[j].strip()]
                    surround  = prev_lens + next_lens
                    if surround:
                        ratio = sum(surround) / len(surround) / max(1, len(s))
                        alpha = sum(c.isalpha() for c in s) / len(s)
                        if ratio >= 5.0 and alpha >= 0.70:
                            conf = 60

            if conf == 0:
                continue

            key = (page_num, sl[:40])
            if key in seen:
                continue
            seen.add(key)

            headings.append({
                "page":          page_num,
                "heading":       s,
                "heading_lower": sl,
                "confidence":    conf,
            })

    # Sort and keep best 2 headings per page
    headings.sort(key=lambda h: (h['page'], -h['confidence']))
    per_page: dict = defaultdict(list)
    for h in headings:
        per_page[h['page']].append(h)
    result = []
    for pg in sorted(per_page.keys()):
        result.extend(per_page[pg][:2])
    return result



def assign_category(text_lower: str) -> str:
    for cat, patterns in SECTION_CATEGORIES.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                return cat
    return "General Information"


def build_chunks(pages: dict, sections: list, doc_name: str,
                 chunk_size: int = 350, overlap: int = 80) -> list:
    section_map     = {s["page"]: s["heading"] for s in sections}
    current_section = "General Information"
    chunks          = []
    for page_num in sorted(pages.keys()):
        if page_num in section_map:
            current_section = section_map[page_num]
        words = pages[page_num].split()
        if not words:
            continue
        step = max(1, chunk_size - overlap)
        for start in range(0, max(1, len(words) - chunk_size + 1), step):
            chunk_text = " ".join(words[start: start + chunk_size])
            if len(chunk_text.strip()) < 40:
                continue
            chunks.append({
                "page":     page_num,
                "section":  current_section,
                "category": assign_category(current_section.lower()),
                "text":     chunk_text,
                "doc_name": doc_name,
            })
    return chunks


def generate_questions(sections: list, chunks: list) -> dict:
    found: dict = {}
    for s in sections:
        hl = s["heading_lower"]
        for pattern, question in QUESTION_TEMPLATES:
            if re.search(pattern, hl) and question not in found:
                found[question] = {"section": s["heading"], "page": s["page"],
                                   "category": assign_category(hl)}
    for chunk in chunks:
        cl = chunk["text"].lower()
        for pattern, question in QUESTION_TEMPLATES:
            if re.search(pattern, cl) and question not in found:
                found[question] = {"section": chunk["section"], "page": chunk["page"],
                                   "category": assign_category(cl[:100])}
    by_cat: dict = {}
    for q, meta in found.items():
        by_cat.setdefault(meta["category"], []).append(
            {"question": q, "section": meta["section"], "page": meta["page"]}
        )
    order = list(SECTION_CATEGORIES.keys()) + ["General Information"]
    return {k: by_cat[k] for k in order if k in by_cat}


# ── Smart answer enrichment ───────────────────────────────────────────────────

def get_plain_answer(query: str) -> str:
    ql = query.lower()
    for pattern, answer in PLAIN_ANSWERS.items():
        if re.search(pattern, ql):
            return answer
    return ""


def get_action_line(query: str) -> str:
    ql = query.lower()
    for pattern, action in ACTION_LINES.items():
        if re.search(pattern, ql):
            return action
    return ""


def extract_bullets(text: str, max_bullets: int = 3) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    key_terms = ["must", "shall", "required", "right", "parent", "school",
                 "evaluation", "consent", "iep", "placement", "days", "notify",
                 "request", "provide", "written", "meeting", "eligible", "service"]
    scored = []
    for s in sentences:
        sl    = s.lower()
        score = sum(1 for t in key_terms if t in sl) + (1 if len(s) < 200 else 0)
        scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    cleaned = []
    for _, b in scored[:max_bullets]:
        b = re.sub(r'\s+', ' ', b).strip()
        b = re.sub(r'^\d+\s+', '', b)
        if b and len(b) > 20:
            cleaned.append(b)
    return cleaned


# ── Search ────────────────────────────────────────────────────────────────────

def _similar(a: str, b: str, threshold: float = 0.6) -> bool:
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb:
        return False
    return len(wa & wb) / max(len(wa), len(wb)) > threshold


def search_all_chunks(query: str, top_k: int = 6) -> list:
    """Search across ALL loaded documents. Returns results tagged with doc_name."""
    all_chunks = st.session_state.get("all_chunks", [])
    if not all_chunks or not query.strip():
        return []
    query_lower = query.lower()
    query_terms = re.findall(r'\w+', query_lower)
    results = []
    for chunk in all_chunks:
        tl     = chunk["text"].lower()
        exact  = 10 if query_lower in tl else 0
        tf     = sum(tl.count(t) for t in query_terms if len(t) > 2)
        domain = sum(w for kw, w in IEP_DOMAIN_WEIGHTS.items() if kw in tl)
        sec_b  = 3 if any(t in chunk["section"].lower() for t in query_terms) else 0
        score  = tf + exact + domain + sec_b
        if score > 0:
            results.append({**chunk, "score": score})
    results.sort(key=lambda x: x["score"], reverse=True)
    deduped, seen = [], []
    for r in results:
        snip = r["text"][:120].lower()
        if not any(_similar(snip, s) for s in seen):
            deduped.append(r)
            seen.append(snip)
        if len(deduped) >= top_k:
            break
    return deduped


def group_by_doc(results: list) -> dict:
    grouped: dict = {}
    for r in results:
        grouped.setdefault(r.get("doc_name", "Unknown"), []).append(r)
    return grouped


def highlight(text: str, query: str, max_chars: int = 500) -> str:
    tl    = text.lower()
    words = query.lower().split()
    pos   = tl.find(words[0]) if words else 0
    start = max(0, pos - 80)
    snip  = text[start: start + max_chars]
    if start > 0:          snip = "…" + snip
    if start + max_chars < len(text): snip += "…"
    for term in sorted(re.findall(r'\w{3,}', query), key=len, reverse=True)[:6]:
        snip = re.sub(rf'\b({re.escape(term)})\b',
                      r'<mark style="background:#FFF176;border-radius:2px;padding:0 1px;">\1</mark>',
                      snip, flags=re.IGNORECASE)
    return snip


def get_related(question: str, all_questions: dict, current_category: str, n: int = 3) -> list:
    return [q for q in all_questions.get(current_category, [])
            if q["question"] != question][:n]


# ── Session helpers ───────────────────────────────────────────────────────────

def init_session():
    defaults = {
        "docs":           {},    # {filename: {pages, chunks, sections, questions}}
        "all_chunks":     [],    # flat list of all chunks across all docs
        "pdf_questions":  {},    # merged question bank
        "pdf_loaded":     False,
        "active_q":       "",
        "active_cat":     "",
        "search_results": [],
        "history":        [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _rebuild_combined():
    all_chunks: list = []
    merged_q:   dict = {}
    for doc_name, doc_data in st.session_state.docs.items():
        all_chunks.extend(doc_data["chunks"])
        for cat, qs in doc_data["questions"].items():
            merged_q.setdefault(cat, [])
            for q in qs:
                if not any(x["question"] == q["question"] for x in merged_q[cat]):
                    merged_q[cat].append(q)
    order = list(SECTION_CATEGORIES.keys()) + ["General Information"]
    st.session_state.all_chunks    = all_chunks
    st.session_state.pdf_questions = {k: merged_q[k] for k in order if k in merged_q}
    st.session_state.pdf_loaded    = bool(all_chunks)


def load_pdf_to_session(file_obj, name: str) -> bool:
    if name in st.session_state.docs:
        return True
    with st.spinner(f"Reading {name}…"):
        pages = extract_pdf(file_obj)
    if not pages:
        return False
    with st.spinner(f"Indexing {name}…"):
        sections  = detect_sections(pages)
        chunks    = build_chunks(pages, sections, doc_name=name)
        questions = generate_questions(sections, chunks)
    st.session_state.docs[name] = {
        "pages": pages, "chunks": chunks,
        "sections": sections, "questions": questions,
    }
    _rebuild_combined()
    return True


def remove_doc(name: str):
    if name in st.session_state.docs:
        del st.session_state.docs[name]
    _rebuild_combined()
    st.session_state.search_results = []
    st.session_state.history        = []
    st.session_state.active_q       = ""


def clear_all_docs():
    st.session_state.docs            = {}
    st.session_state.all_chunks      = []
    st.session_state.pdf_questions   = {}
    st.session_state.pdf_loaded      = False
    st.session_state.search_results  = []
    st.session_state.history         = []
    st.session_state.active_q        = ""
    st.session_state.active_cat      = ""


def auto_load_from_docs():
    if st.session_state.pdf_loaded:
        return True
    for pdf_path in DOCS_DIR.glob("*.pdf"):
        load_pdf_to_session(pdf_path, pdf_path.name)
    return st.session_state.pdf_loaded


# ── Backward-compat wrapper so other pages keep working ──────────────────────
def search_chunks(_ignored, query: str, top_k: int = 5,
                  section_filter: str = "") -> list:
    results = search_all_chunks(query, top_k=top_k * 2)
    if section_filter:
        results = [r for r in results if section_filter.lower() in r["section"].lower()]
    return results[:top_k]
