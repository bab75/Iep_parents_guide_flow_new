# IEP Parent Guide

A free, parent-friendly Streamlit app that turns your IEP Standard Operating
Procedures PDF into plain-English answers, visual guides and checklists.

**No API key. No subscription. No cost. Ever.**

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Open http://localhost:8501 → Upload your PDF → Explore.

---

## How It Works

1. You upload your IEP SOP PDF (any state, any district)
2. The app reads every page, detects section headings, and builds a question bank
3. Every question links to the exact passage and page number in your document
4. No AI writing answers — everything shown is directly from your PDF

---

## Pages

| Page | What it does |
|---|---|
| Home | Upload PDF, orientation, where to start |
| Ask Questions | Click auto-generated questions or type your own — answers from your PDF |
| Flowchart | Visual step-by-step IEP journey — click any step to see your document |
| Cheat Sheet | Every section of your PDF as a plain-English card |
| My Timeline | Enter consent date → see your 60-day deadline and milestones |
| My Rights | All parent rights — what they mean, what to say, what to do |
| Glossary | Every IEP term explained in plain English |

---

## Project Structure

```
iep_parent_app/
├── Home.py                    ← Entry point (streamlit run Home.py)
├── requirements.txt
├── README.md
├── pages/
│   ├── 01_Ask_Questions.py
│   ├── 02_Flowchart.py
│   ├── 03_Cheat_Sheet.py
│   ├── 04_My_Timeline.py
│   ├── 05_My_Rights.py
│   └── 06_Glossary.py
├── utils/
│   ├── rag_engine.py          ← PDF extraction, section detection, search
│   └── theme.py               ← Shared styles and components
└── docs/                      ← Place PDF here for auto-load
```

---

## GitHub & Hosting

```bash
git init && git add . && git commit -m "IEP Parent Guide"
git remote add origin https://github.com/YOUR/iep-parent-guide.git
git push -u origin main
```

Deploy free on Streamlit Community Cloud: share.streamlit.io

---

## Privacy

Your PDF is read locally. It is never sent to any server or third party.
All processing happens on your machine or on Streamlit Community Cloud.
