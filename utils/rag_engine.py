"""
IEP Parent App — Universal RAG Engine (v3)

DESIGN PRINCIPLE: Zero hardcoding for any specific PDF.
Every piece of structure — section names, page numbers, topic mapping —
is learned from whatever PDF the user uploads.

Works for: NYC DOE SOPM, any US state IEP SOP, any updated version,
           any other special education policy document.

Steps:
  1. Extract text from every page (pdfplumber → PyMuPDF fallback)
  2. Parse the Table of Contents from the PDF to get real section name → page pairs
  3. Detect headings on every page using multiple strategies
  4. Build chunks with correct section labels
  5. Generate questions by matching question templates against detected headings
  6. Build a dynamic section→topic index for smart search scoring
  7. Search using: term frequency + section match boost + topic map boost
"""

import re
import streamlit as st
from pathlib import Path
from collections import defaultdict

DOCS_DIR = Path(__file__).parent.parent / "docs"

# ── IEP question templates (universal — based on federal IDEA law) ────────────
QUESTION_TEMPLATES = [
    (r"referral",                        "How does the referral process work?"),
    (r"child find",                      "What is Child Find and who does it cover?"),
    (r"consent",                         "When is parental consent required?"),
    (r"evaluat",                         "What happens during the evaluation?"),
    (r"60.day|timeline|timeframe",       "What is the 60-day timeline?"),
    (r"eligib",                          "How is eligibility for special education determined?"),
    (r"classif",                         "What disability classifications are used?"),
    (r"iep meeting|meeting",             "What happens at an IEP meeting?"),
    (r"iep team|team comp",              "Who is on the IEP team?"),
    (r"present level",                   "What are Present Levels of Performance?"),
    (r"annual goal",                     "What are annual goals and how are they written?"),
    (r"service",                         "What special education services are available?"),
    (r"related service",                 "What are related services?"),
    (r"placement",                       "How is a placement decided?"),
    (r"least restrict|lre",              "What is Least Restrictive Environment (LRE)?"),
    (r"accommodat",                      "What accommodations can be put in an IEP?"),
    (r"modif",                           "What modifications can be made?"),
    (r"annual review",                   "How often is the IEP reviewed?"),
    (r"reevaluat",                       "When does my child get reevaluated?"),
    (r"amend",                           "How can an IEP be changed between annual reviews?"),
    (r"prior written|pwn",               "What is Prior Written Notice?"),
    (r"procedural safeguard|parent right","What are my rights as a parent?"),
    (r"independent.*eval|iee",           "Can I get an Independent Educational Evaluation?"),
    (r"mediat",                          "How does mediation work?"),
    (r"complaint|due process",           "What can I do if I disagree with the IEP?"),
    (r"transition",                      "What is transition planning?"),
    (r"extend.*school|esy",              "What is Extended School Year (ESY)?"),
    (r"behavior|bip|fba",                "What is a Behavioral Intervention Plan?"),
    (r"paraprofessional|para",           "When does a student get a paraprofessional?"),
    (r"transport",                       "What transportation services are available?"),
    (r"notif",                           "When must the school notify me?"),
    (r"record",                          "How do I get my child's school records?"),
    (r"surrogate",                       "What is a surrogate parent?"),
    (r"transfer",                        "What happens to the IEP when my child transfers schools?"),
    (r"home instruct",                   "What is home instruction?"),
    (r"interim|pendency",                "What happens to services during a dispute?"),
    (r"discipline|suspend",              "What are the rules around discipline for students with IEPs?"),
    (r"manifestat",                      "What is a Manifestation Determination Review?"),
    (r"social histor",                   "What is a Social History Interview?"),
    (r"assistive tech",                  "What assistive technology support is available?"),
    (r"12.month|summer",                 "Can my child receive summer services?"),
    (r"preschool|early",                 "Are there special education services for preschool children?"),
    (r"graduation|exit|diploma",         "What are the graduation options for students with IEPs?"),
    (r"charter",                         "What about students in charter schools?"),
    (r"private.*school|parochial",       "What are the rules for students in private schools?"),
]

# ── Section display categories (universal IEP topics) ────────────────────────
SECTION_CATEGORIES = {
    "Getting Started":  [r"referral", r"child find", r"overview", r"introduction", r"purpose", r"welcome"],
    "Timelines":        [r"timeline", r"timeframe", r"60.day", r"deadline", r"calendar", r"days"],
    "Evaluation":       [r"evaluat", r"assess", r"test", r"social histor", r"psycho", r"bilingual"],
    "Eligibility":      [r"eligib", r"classif", r"disability", r"determin"],
    "The IEP Document": [r"iep", r"present level", r"annual goal", r"service", r"accommodat", r"modif",
                         r"postsecondary", r"transition need"],
    "Placement":        [r"placement", r"least restrict", r"lre", r"continuum", r"program", r"recommend"],
    "Parent Rights":    [r"parent right", r"procedural", r"consent", r"notice", r"pwn", r"record",
                         r"iee", r"independent", r"safeguard"],
    "Meetings":         [r"meeting", r"team", r"committee", r"cse", r"case manager"],
    "Disagreements":    [r"mediat", r"complaint", r"due process", r"dispute", r"appeal", r"hearing",
                         r"impartial", r"resolution"],
    "Special Topics":   [r"transition", r"esy", r"behavior", r"bip", r"fba", r"transport",
                         r"discipline", r"suspend", r"assistive", r"paraprofessional",
                         r"graduation", r"exit", r"charter", r"private", r"temporary housing"],
}

# ── Plain-English answer templates (based on federal IDEA — universal) ────────
PLAIN_ANSWERS = {
    r"referral":               "A referral is the very first step. You or the school ask in writing for a special education evaluation. You do not need a specific reason — if you think your child may need help, you have the right to ask.",
    r"child find":             "Child Find is the legal obligation for every school district to identify, locate, and evaluate children with disabilities — including children not currently in school, homeless children, and children in private schools.",
    r"consent":                "The school must get your written permission before doing anything — before any evaluation and before any placement change. You can say yes to some parts and no to others.",
    r"60.day|timeline":        "Once you sign the consent form, the school has 60 school days to complete all evaluations AND hold the IEP meeting. This is a strict legal deadline.",
    r"eligib":                 "After evaluations, the full team — including you — meets to decide if your child qualifies under one of 13 disability categories. You are an equal member of this team.",
    r"evaluat":                "A team of specialists evaluates your child in every area where a disability is suspected. They must use more than one test and cannot rely on a single result to make any decision.",
    r"placement":              "Placement is where and how your child will be educated. The law requires the Least Restrictive Environment — your child must be with non-disabled peers as much as possible.",
    r"least restrict|lre":     "Your child must be educated alongside non-disabled students as much as their needs allow. A more separate setting requires written justification from the team.",
    r"prior written|pwn":      "Before the school changes, proposes, or refuses anything about your child's IEP, they must give you a written notice explaining exactly what they are doing and why.",
    r"parent right|procedural":"You have rights at every step: to be part of every decision, get written notice before any changes, see all school records, and disagree through mediation or a formal complaint.",
    r"annual review":          "The IEP must be reviewed at least once every year. The team checks your child's progress, updates goals, and revises services. You are invited and your input matters.",
    r"reevaluat":              "Every 3 years the school does a full reevaluation to check whether your child still qualifies and what their current needs are. You can also request one earlier.",
    r"mediat":                 "Mediation is a free, voluntary process where a neutral person helps you and the school reach an agreement. It is faster and less stressful than a formal hearing.",
    r"iep meeting":            "The IEP meeting is where the team writes or reviews your child's education plan. You are a required member. The meeting cannot finalize the plan without making reasonable efforts to include you.",
    r"transition":             "For students aged 15 and older, the IEP must include measurable goals for life after school — college, employment, or independent living — and services to reach those goals.",
    r"service":                "Special education services are specialized instruction designed for your child's unique needs. The IEP must specify the type, frequency, duration, and setting for each service.",
    r"related service":        "Related services like speech therapy, occupational therapy, physical therapy, and counseling support your child in benefiting from their main special education program.",
    r"complaint|due process":  "If you disagree with any IEP decision, you have three options: free mediation, a state complaint filed with the education department, or a formal due process hearing.",
    r"record":                 "You have the right to inspect and get copies of all your child's school records — evaluations, IEPs, progress reports — within 45 days, at no cost to you.",
    r"annual goal":            "Annual goals are specific, measurable targets your child should reach within one year. A proper goal has a starting point, a target, and a clear way to measure progress.",
    r"iee":                    "If you disagree with the school's evaluation, you can request an Independent Educational Evaluation done by someone outside the school, paid for by the school district.",
    r"behavior|bip":           "A Behavioral Intervention Plan uses positive strategies to address challenging behaviors. It must be based on a Functional Behavioral Assessment (FBA) completed first.",
    r"esy":                    "Extended School Year provides services during summer or school breaks for students who would lose significant skills without year-round support.",
    r"social histor":          "A Social History Interview is a meeting with the school social worker where your child's background is discussed and your rights as a parent are explained.",
    r"discipline|suspend":     "Students with IEPs have special discipline protections. Schools must determine if a behavior is related to the disability before making long-term discipline decisions.",
    r"graduation|exit":        "Students with IEPs have multiple graduation pathways and credential options. The IEP team helps plan the right path based on the student's goals and abilities.",
    r"surrogate":              "A surrogate parent is appointed when no parent can be found or identified. They have all the same rights as a parent in the IEP process.",
}

ACTION_LINES = {
    r"referral":               "Write a dated letter to the school requesting an evaluation. Keep a copy — the date you submit it starts the official process.",
    r"consent":                "Read the consent form carefully before signing. You can ask questions first. You are not required to sign the same day it is given to you.",
    r"60.day|timeline":        "Note the exact date you signed consent. Count 60 school days forward — that is the legal deadline for the IEP meeting to happen.",
    r"eligib":                 "Bring your own information, reports, or outside evaluations to the eligibility meeting. Your input must be considered by the team.",
    r"evaluat":                "Ask for copies of all evaluation reports at least a few days before the meeting so you have time to review them carefully.",
    r"placement":              "Ask the team: What less restrictive option was considered, and why was it rejected? They must document this answer.",
    r"prior written|pwn":      "If the school proposes any change, request Prior Written Notice in writing before agreeing. Do not accept verbal explanations alone.",
    r"parent right|procedural":"Ask for a copy of the Procedural Safeguards notice at every meeting. It lists all your legal rights and how to use them.",
    r"annual review":          "Before the annual review, request your child's progress reports so you can review them ahead of time and come prepared.",
    r"mediat":                 "Mediation is free and does not give up your other legal rights. It is often a good first step before filing a formal complaint.",
    r"record":                 "Send a written request for records by email or letter and keep a copy. Schools must respond within 45 days.",
    r"complaint|due process":  "Document every communication with the school in writing. This documentation is essential if you need to file a formal complaint.",
    r"iee":                    "Send a written request for an IEE to the school. They must either agree to pay for it or immediately file for a hearing to defend their evaluation.",
    r"transition":             "If your child is 14 or 15, raise transition planning at the next IEP meeting even if the school has not brought it up.",
    r"annual goal":            "Review each goal and ask: How will we know if this goal is met? Who measures it, and how often will I get updates?",
    r"social histor":          "The Social History Interview is your first opportunity to share important information about your child. Prepare notes beforehand.",
    r"discipline|suspend":     "If the school wants to suspend or remove your child for more than 10 days, request a Manifestation Determination Review meeting immediately.",
}

# ── IEP domain weights for search scoring ────────────────────────────────────
IEP_DOMAIN_WEIGHTS = {
    "iep": 3, "evaluation": 2, "eligibility": 2, "placement": 2,
    "annual review": 3, "amendment": 2, "consent": 2, "disability": 1,
    "services": 1, "least restrictive": 3, "lre": 3, "transition": 2,
    "prior written notice": 3, "pwn": 3, "parent": 1, "goals": 1,
    "present levels": 2, "fape": 3, "idea": 2, "referral": 2,
    "60 day": 3, "reevaluation": 2, "procedural": 2, "mediation": 2,
    "due process": 3, "discipline": 1, "bip": 2, "fba": 2,
}


# ═══════════════════════════════════════════════════════════════════════════════
# PDF EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_pdf(file_obj) -> dict:
    """Extract {page_num: text} — tries pdfplumber then PyMuPDF."""
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


# ═══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL TOC PARSER
# Reads the actual Table of Contents from the PDF to get heading → page mapping.
# Works for any PDF that has a TOC — does not assume page numbers.
# ═══════════════════════════════════════════════════════════════════════════════

def parse_toc_from_pages(pages: dict) -> dict:
    """
    Universal TOC parser. Returns {heading_lower: page_number}.

    Strategy 1: Standard TOC with printed page numbers.
    Strategy 2: Hyperlink-only TOC (no page numbers) — extracts heading names
                from TOC pages then locates them in body text.
                Handles two-column PDF layouts like NYC DOE SOPM.
    """
    max_page = max(pages.keys())
    toc_map  = {}

    # ── Strategy 1: lines ending with page numbers ────────────────────────────
    TOC_ENTRY  = re.compile(r'(.{5,70}?)[\s\.·•\-]{2,}(\d{1,3})\s*$', re.M)
    TOC_INLINE = re.compile(r'(.{5,60}?)\s{4,}(\d{1,3})\s*$', re.M)
    TOC_TAB    = re.compile(r'(.{5,60}?)\t(\d{1,3})\s*$', re.M)

    for pg_num in range(1, min(11, max_page + 1)):
        text = pages.get(pg_num, "")
        for pat in [TOC_ENTRY, TOC_INLINE, TOC_TAB]:
            for m in pat.finditer(text):
                h = re.sub(r'^[\d\.\)\-\s]+', '', m.group(1).strip()).strip()
                try:
                    p = int(m.group(2))
                    if len(h) >= 4 and 1 <= p <= max_page:
                        toc_map[h.lower()] = p
                except ValueError:
                    pass

    if toc_map:
        return toc_map  # Standard TOC found — done

    # ── Strategy 2: Hyperlink-only TOC (no printed page numbers) ─────────────
    # Step A: identify TOC pages
    SKIP_TOC = re.compile(
        r'Table of Contents|click on a title|navigate to|^\d+\s*[|]', re.I
    )
    toc_pages = []
    for pg_num in range(1, min(11, max_page + 1)):
        text  = pages.get(pg_num, "")
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if len(lines) < 10:
            continue
        avg = sum(len(l) for l in lines) / len(lines)
        if avg < 70:
            toc_pages.append(pg_num)

    if not toc_pages:
        return toc_map

    # Step B: extract candidate heading names from TOC pages
    candidates = set()
    for pg_num in toc_pages:
        for line in pages[pg_num].split("\n"):
            s = line.strip()
            if not s or len(s) < 5 or len(s) > 80 or SKIP_TOC.search(s):
                continue
            alpha = sum(c.isalpha() for c in s) / len(s)
            if alpha < 0.65:
                continue
            # Split on 3+ spaces (handles two-column layouts)
            parts = re.split(r'\s{3,}', s)
            for part in parts:
                part = part.strip()
                if (4 <= len(part) <= 75
                        and sum(c.isalpha() for c in part) / max(1, len(part)) > 0.65):
                    candidates.add(part)

    # Step C: locate each candidate in body pages
    body_start = max(toc_pages) + 1
    for heading in candidates:
        hl = heading.lower()
        for pg_num in range(body_start, max_page + 1):
            for line in pages[pg_num].split("\n"):
                l = line.strip()
                if l.lower() == hl or (l.lower().startswith(hl) and len(l) < len(heading) + 15):
                    toc_map[hl] = pg_num
                    break
            if hl in toc_map:
                break

    return toc_map

def assign_category(text_lower: str) -> str:
    """Map text to a display category using universal IEP topic patterns."""
    for cat, patterns in SECTION_CATEGORIES.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                return cat
    return "General Information"


def detect_sections(pages: dict) -> list:
    """
    Universal section detector — works for any PDF.

    Priority order:
    1. TOC-derived sections (highest confidence) — reads actual TOC from PDF
    2. ALL CAPS headings on body pages
    3. Short lines between long body text (ratio-based)
    4. Lines that start at same position as known headings (visual indent)
    """
    # Step 1: parse TOC to get real section → page mapping
    toc_map = parse_toc_from_pages(pages)  # {heading_lower: page_num}

    headings = []
    seen = set()

    # Step 2: inject all TOC-derived headings with high confidence
    for heading_lower, page_num in toc_map.items():
        # Convert lowercase back to title case for display
        heading_display = heading_lower.title()
        # Try to find the actual casing in the page text
        page_text = pages.get(page_num, "")
        for line in page_text.split("\n"):
            l = line.strip()
            if l.lower() == heading_lower or l.lower().startswith(heading_lower[:20]):
                heading_display = l
                break

        key = (page_num, heading_lower[:40])
        if key not in seen:
            seen.add(key)
            headings.append({
                "page":          page_num,
                "heading":       heading_display,
                "heading_lower": heading_lower,
                "confidence":    90,
                "source":        "toc",
            })

    # Step 3: scan body pages for additional headings not in TOC
    ALL_CAPS = re.compile(r'^[A-Z][A-Z\s\-\/\(\)&]{4,79}$')
    SKIP = re.compile(
        r'^\d+\s*[|]\s*'   # page footers like "12 | Document Name"
        r'|^Table of Contents'
        r'|^\d+$'
        r'|^[•\-\*]'
    )

    # Build set of pages already covered by TOC
    toc_pages_covered = {v for v in toc_map.values()}

    for page_num in sorted(pages.keys()):
        text = pages[page_num]
        lines = text.split("\n")
        n = len(lines)

        # Strip repeating header/footer from lines for analysis
        clean_lines = []
        for line in lines:
            l = line.strip()
            if not l or SKIP.search(l):
                continue
            # Skip lines that are the TOC nav bar repeated on every page
            # (detected by: very short content surrounded by page-range numbers)
            clean_lines.append(l)

        for i, s in enumerate(clean_lines):
            if len(s) < 5 or len(s) > 85:
                continue
            sl = s.lower().strip()
            conf = 0

            # ALL CAPS heading
            if ALL_CAPS.match(s) and len(s) >= 6:
                conf = 80

            # Short line with high surrounding-length ratio (heading in body text)
            elif 8 <= len(s) <= 60:
                # Get context lines
                ctx_before = clean_lines[max(0, i-2):i]
                ctx_after  = clean_lines[i+1:min(len(clean_lines), i+3)]
                ctx_lens   = [len(l) for l in ctx_before + ctx_after if l]
                if ctx_lens:
                    avg_ctx = sum(ctx_lens) / len(ctx_lens)
                    alpha   = sum(c.isalpha() for c in s) / len(s)
                    ratio   = avg_ctx / max(1, len(s))
                    bad_end = any(s.endswith(e) for e in
                                  ['.', ',', ';', ')', ':', 'and', 'or', 'the', 'a'])
                    starts_cap = s[0].isupper()

                    if (ratio >= 5.0 and alpha >= 0.70
                            and not bad_end and starts_cap
                            and len(s.split()) >= 2):
                        conf = 60

            if conf == 0:
                continue

            key = (page_num, sl[:40])
            if key not in seen:
                seen.add(key)
                headings.append({
                    "page":          page_num,
                    "heading":       s,
                    "heading_lower": sl,
                    "confidence":    conf,
                    "source":        "body",
                })

    # Sort by page, then confidence desc
    headings.sort(key=lambda h: (h["page"], -h["confidence"]))

    # Keep best 2 per page
    per_page: dict = defaultdict(list)
    for h in headings:
        per_page[h["page"]].append(h)


    # ── Extra pass: check first content line of each page after stripping nav ──
    # Many PDFs (like NYC DOE SOPM) have section headings as the FIRST line
    # on a new page, immediately after the repeated nav header.
    # NAV patterns that appear on every page (discovered dynamically)
    from collections import Counter
    nav_counter = Counter()
    for text in pages.values():
        first = text.split("\n")[:3]
        for l in first:
            ls = l.strip()
            if 10 <= len(ls) <= 120:
                nav_counter[ls] += 1
    nav_thresh = max(3, len(pages) * 0.25)
    nav_set = {l for l, c in nav_counter.items() if c >= nav_thresh}

    GOOD_HEADING = re.compile(r'^[A-Z][A-Za-z\s\-\/\(\)&\'\,\.]{4,79}$')
    GOOD_HEADING = re.compile(r'^[A-Z][A-Za-z\s\-\/\(\)&\'\,\.]{4,79}$')
    BAD_END      = re.compile(r'[,;]$')
    for page_num in sorted(pages.keys()):
        if page_num in {s["page"] for s in headings}:
            continue  # already have a heading for this page
        lines_pg = [l.strip() for l in pages[page_num].split("\n")
                    if l.strip() and l.strip() not in nav_set]
        if not lines_pg:
            continue
        first_line = lines_pg[0]
        if (GOOD_HEADING.match(first_line)
                and not BAD_END.search(first_line)
                and len(first_line.split()) >= 2
                and len(first_line) <= 75):
            key = (page_num, first_line.lower()[:40])
            if key not in seen:
                seen.add(key)
                headings.append({
                    "page":          page_num,
                    "heading":       first_line,
                    "heading_lower": first_line.lower(),
                    "confidence":    75,
                    "source":        "first_line",
                })

    result = []
    for pg in sorted(per_page.keys()):
        result.extend(per_page[pg][:2])

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CHUNKING
# Strips repeated navigation text before chunking.
# Limits section label carryover to 6 pages maximum.
# ═══════════════════════════════════════════════════════════════════════════════

def _build_nav_stripper(pages: dict):
    """
    Detect the repeating navigation header/footer pattern in this specific PDF
    and return a regex to strip it.
    Works by finding lines that appear verbatim on 5+ pages near the top.
    """
    # Count line occurrences across first lines of each page
    from collections import Counter
    line_counts = Counter()
    for text in pages.values():
        first_lines = text.split("\n")[:3]
        for line in first_lines:
            l = line.strip()
            if 10 <= len(l) <= 120:
                line_counts[l] += 1

    # Lines appearing on >30% of pages are navigation headers
    threshold = max(3, len(pages) * 0.3)
    nav_lines = [l for l, count in line_counts.items() if count >= threshold]

    if not nav_lines:
        return None

    # Build regex to strip these lines
    patterns = [re.escape(l) for l in nav_lines]
    combined = '|'.join(f'(?:{p})' for p in patterns)
    return re.compile(combined + r'[^\n]*\n?', re.MULTILINE)


def _strip_page_footer(text: str) -> str:
    """Remove common page footer patterns like '12 | Document Name...'"""
    return re.sub(r'\d+\s*[|]\s*[A-Z][^\n]*', '', text)


def build_chunks(pages: dict, sections: list, doc_name: str,
                 chunk_size: int = 350, overlap: int = 80) -> list:
    """
    Build overlapping word-chunks from body pages.
    - Detects and strips repeating nav headers automatically
    - Skips TOC-only pages (detected by high ratio of short lines)
    - Limits section label carryover to 6 pages
    """
    # Build section map: page → heading
    section_map = {s["page"]: s["heading"] for s in sections}

    # Detect repeating nav header for this specific PDF
    nav_stripper = _build_nav_stripper(pages)

    # Detect TOC-only pages (avg line length < 55 and many lines)
    toc_pages = set()
    for pg, text in pages.items():
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if len(lines) < 10:
            continue
        avg_len = sum(len(l) for l in lines) / len(lines)
        # Short lines AND many lines = likely TOC
        if avg_len < 55 and len(lines) > 25:
            toc_pages.add(pg)

    current_section   = "General Information"
    last_heading_page = 0
    chunks            = []

    for page_num in sorted(pages.keys()):
        if page_num in toc_pages:
            continue

        # Update section from map
        if page_num in section_map:
            current_section   = section_map[page_num]
            last_heading_page = page_num
        elif (page_num - last_heading_page) > 6:
            # Section hasn't changed in 6 pages — reset to avoid wrong labels
            current_section = "General Information"

        # Clean the page text
        page_text = pages[page_num]
        if nav_stripper:
            page_text = nav_stripper.sub("", page_text)
        page_text = _strip_page_footer(page_text).strip()

        words = page_text.split()
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


# ═══════════════════════════════════════════════════════════════════════════════
# DYNAMIC SECTION-TOPIC INDEX
# Built from whatever headings are actually in the PDF.
# No hardcoded section names.
# ═══════════════════════════════════════════════════════════════════════════════

def build_section_topic_index(sections: list) -> dict:
    """
    Build a mapping: section_heading_lower → [topic_keywords]
    by matching each detected section heading against question template patterns.

    This replaces the hardcoded SECTION_TOPIC_MAP with something
    derived entirely from the PDF's own structure.

    Returns: {section_lower: [keyword, ...]}
    """
    index = {}
    for s in sections:
        hl = s["heading_lower"]
        matched_keywords = []

        # Match against question templates to find what topic this section covers
        for pattern, question in QUESTION_TEMPLATES:
            if re.search(pattern, hl):
                # Extract keywords from the question itself
                kw_terms = re.findall(r'\w{4,}', question.lower())
                stopwords = {"what", "when", "does", "have", "does", "this",
                             "that", "from", "with", "your", "their", "which",
                             "child", "student"}  # too generic to boost
                matched_keywords.extend(
                    [t for t in kw_terms if t not in stopwords]
                )

        # Also include significant words from the heading itself
        heading_words = [w for w in re.findall(r'\w{4,}', hl)
                         if w not in {"with", "from", "that", "this", "have",
                                      "been", "will", "when", "what", "does"}]
        matched_keywords.extend(heading_words)

        if matched_keywords:
            index[hl] = list(set(matched_keywords))

    return index


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION GENERATION
# Matches question templates against headings actually found in the PDF.
# ═══════════════════════════════════════════════════════════════════════════════

def generate_questions(sections: list, chunks: list) -> dict:
    """
    Generate question bank from headings found in this specific PDF.
    No hardcoded assumptions about what sections exist.
    """
    found: dict = {}

    # Match question templates against detected section headings
    for s in sections:
        hl = s["heading_lower"]
        for pattern, question in QUESTION_TEMPLATES:
            if re.search(pattern, hl) and question not in found:
                found[question] = {
                    "section":  s["heading"],
                    "page":     s["page"],
                    "category": assign_category(hl),
                }

    # Also scan chunk content for topics not covered by headings
    for chunk in chunks:
        cl = chunk["text"].lower()
        for pattern, question in QUESTION_TEMPLATES:
            if re.search(pattern, cl) and question not in found:
                found[question] = {
                    "section":  chunk["section"],
                    "page":     chunk["page"],
                    "category": assign_category(cl[:100]),
                }

    # Group by category
    by_cat: dict = {}
    for q, meta in found.items():
        by_cat.setdefault(meta["category"], []).append({
            "question": q,
            "section":  meta["section"],
            "page":     meta["page"],
        })

    order = list(SECTION_CATEGORIES.keys()) + ["General Information"]
    return {k: by_cat[k] for k in order if k in by_cat}


# ═══════════════════════════════════════════════════════════════════════════════
# ANSWER ENRICHMENT (universal — based on IDEA federal law)
# ═══════════════════════════════════════════════════════════════════════════════

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
    """Extract most informative sentences as bullet points."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    key_terms = ["must", "shall", "required", "right", "parent", "school",
                 "evaluation", "consent", "iep", "placement", "days", "notify",
                 "request", "provide", "written", "meeting", "eligible", "service"]
    scored = [(sum(1 for t in key_terms if t in s.lower()) + (1 if len(s) < 200 else 0), s)
              for s in sentences]
    scored.sort(key=lambda x: x[0], reverse=True)
    cleaned = []
    for _, b in scored[:max_bullets]:
        b = re.sub(r'\s+', ' ', b).strip()
        b = re.sub(r'^\d+\s+', '', b)
        if b and len(b) > 20:
            cleaned.append(b)
    return cleaned


# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH
# Scoring uses dynamic section-topic index, not hardcoded section names.
# ═══════════════════════════════════════════════════════════════════════════════

def _similar(a: str, b: str, threshold: float = 0.6) -> bool:
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb:
        return False
    return len(wa & wb) / max(len(wa), len(wb)) > threshold


def search_all_chunks(query: str, top_k: int = 6) -> list:
    """
    Universal search across all loaded documents.

    Scoring:
      1. Exact phrase match in text: +20
      2. Term frequency of meaningful query terms in text
      3. Section heading match:
         - Direct term overlap with section name: +30/+60
         - Dynamic topic index match: +40 per hit
      4. Suppress chunks with no query terms in text
      5. Suppress weak matches where section is unrelated
    """
    all_chunks = st.session_state.get("all_chunks", [])
    if not all_chunks or not query.strip():
        return []

    # Get dynamic section-topic index for this PDF session
    section_index = st.session_state.get("section_topic_index", {})

    query_lower = query.lower()
    stopwords   = {"what", "is", "are", "who", "how", "when", "does", "the",
                   "a", "an", "and", "or", "of", "to", "in", "it", "for",
                   "my", "can", "will", "do", "this", "that", "i", "you",
                   "we", "they", "their", "be", "been", "has", "have",
                   "get", "at", "on", "by", "with", "from", "as", "was"}
    query_terms = [t for t in re.findall(r'\w+', query_lower)
                   if len(t) > 2 and t not in stopwords]

    results = []
    for chunk in all_chunks:
        tl      = chunk["text"].lower()
        sec_low = chunk["section"].lower()

        # Exact phrase match
        exact = 20 if query_lower in tl else 0

        # Term frequency
        tf = sum(tl.count(t) for t in query_terms)

        # Suppress if no query terms found at all
        if tf == 0 and exact == 0:
            continue

        # Section heading match — direct term overlap
        sec_hits = sum(1 for t in query_terms if t in sec_low)
        if sec_hits == 0:
            sec_bonus = 0
        elif sec_hits == 1:
            sec_bonus = 30
        else:
            sec_bonus = 60

        # Dynamic topic index boost
        # Find if any section in the index matches this chunk's section
        topic_bonus = 0
        for idx_sec, idx_words in section_index.items():
            if idx_sec in sec_low or sec_low in idx_sec:
                # This chunk's section is in the index
                # Check how many index words match the query
                hits = sum(1 for w in idx_words if w in query_lower)
                if hits > 0:
                    topic_bonus = max(topic_bonus, 40 * hits)

        # Small domain weight bonus
        domain = sum(w for kw, w in IEP_DOMAIN_WEIGHTS.items() if kw in tl) // 4

        score = tf + exact + sec_bonus + topic_bonus + domain

        # Suppress weak off-topic results
        if sec_bonus == 0 and topic_bonus == 0 and tf < 4 and exact == 0:
            continue

        results.append({**chunk, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)

    # De-duplicate near-identical chunks
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


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def init_session():
    defaults = {
        "docs":                {},
        "all_chunks":          [],
        "pdf_questions":       {},
        "section_topic_index": {},
        "pdf_loaded":          False,
        "active_q":            "",
        "active_cat":          "",
        "search_results":      [],
        "history":             [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _rebuild_combined():
    """Rebuild all_chunks, pdf_questions, and section_topic_index from all loaded docs."""
    all_chunks: list = []
    merged_q:   dict = {}
    merged_idx: dict = {}

    for doc_name, doc_data in st.session_state.docs.items():
        all_chunks.extend(doc_data["chunks"])

        for cat, qs in doc_data["questions"].items():
            merged_q.setdefault(cat, [])
            for q in qs:
                if not any(x["question"] == q["question"] for x in merged_q[cat]):
                    merged_q[cat].append(q)

        # Merge section topic indexes
        for sec, words in doc_data.get("section_index", {}).items():
            if sec not in merged_idx:
                merged_idx[sec] = words
            else:
                merged_idx[sec] = list(set(merged_idx[sec] + words))

    order = list(SECTION_CATEGORIES.keys()) + ["General Information"]
    st.session_state.all_chunks          = all_chunks
    st.session_state.pdf_questions       = {k: merged_q[k] for k in order if k in merged_q}
    st.session_state.section_topic_index = merged_idx
    st.session_state.pdf_loaded          = bool(all_chunks)


def load_pdf_to_session(file_obj, name: str) -> bool:
    """Load a single PDF and add to the multi-doc store."""
    if name in st.session_state.docs:
        return True
    with st.spinner(f"Reading {name}…"):
        pages = extract_pdf(file_obj)
    if not pages:
        return False
    with st.spinner(f"Indexing {name}…"):
        sections      = detect_sections(pages)
        chunks        = build_chunks(pages, sections, doc_name=name)
        questions     = generate_questions(sections, chunks)
        section_index = build_section_topic_index(sections)

    st.session_state.docs[name] = {
        "pages":         pages,
        "chunks":        chunks,
        "sections":      sections,
        "questions":     questions,
        "section_index": section_index,
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
    st.session_state.docs                = {}
    st.session_state.all_chunks          = []
    st.session_state.pdf_questions       = {}
    st.session_state.section_topic_index = {}
    st.session_state.pdf_loaded          = False
    st.session_state.search_results      = []
    st.session_state.history             = []
    st.session_state.active_q            = ""
    st.session_state.active_cat          = ""


def auto_load_from_docs():
    if st.session_state.pdf_loaded:
        return True
    for pdf_path in DOCS_DIR.glob("*.pdf"):
        load_pdf_to_session(pdf_path, pdf_path.name)
    return st.session_state.pdf_loaded


# ── Backward-compat wrapper (other pages call search_chunks) ──────────────────
def search_chunks(_ignored, query: str, top_k: int = 5,
                  section_filter: str = "") -> list:
    results = search_all_chunks(query, top_k=top_k * 2)
    if section_filter:
        results = [r for r in results if section_filter.lower() in r["section"].lower()]
    return results[:top_k]
