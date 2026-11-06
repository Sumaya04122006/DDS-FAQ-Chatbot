---
title: Agentic AI Project Ideas and Idea Validation
doc_type: ideas
last_updated: 2026-11-06
---

# Project Ideas (use as inspiration, don't copy blindly)

## How to choose a good idea
A good challenge idea is: **narrow, real, demo-able in 2 minutes, and clearly agentic.**
Scorecard (rate each 1–5; aim for 16+ out of 20):
1. **Pain:** does a specific person have this problem often?
2. **Feasibility in 8 days:** can the core flow work with 2–4 tools?
3. **Wow in a demo:** can a judge see value in 60 seconds?
4. **Agentic depth:** does the system plan/choose tools/act, not only chat?

## Ideas by domain
### Education
- **Study planner agent:** reads a syllabus PDF (RAG), builds a revision schedule, quizzes the user, adapts to weak topics.
- **Assignment feedback agent:** checks a draft against a rubric and gives structured feedback with citations to the rubric.

### Business / productivity
- **Meeting-to-actions agent:** takes a transcript, extracts tasks, assigns owners, drafts follow-up emails, creates calendar entries (with approval).
- **Invoice/receipt processing agent:** extracts fields from files, validates, writes to a spreadsheet, flags anomalies.
- **Sales lead qualifier:** enriches leads from public data, scores them, drafts personalised outreach for human review.

### Customer support
- **Support triage agent:** classifies tickets, searches the knowledge base, drafts replies, escalates when confidence is low.
- **FAQ agent for a small business:** WhatsApp/web chat answering from the business's documents.

### Data / analytics
- **Talk-to-your-CSV analyst:** converts questions to pandas/SQL, runs safely in a sandbox, charts and explains the result.
- **Report generator agent:** pulls data from several sources and writes a weekly summary.

### Health & wellbeing (information support only, never diagnosis)
- **Medication/appointment reminder organiser** using user-provided schedules.
- **Wellness habit coach** with memory of goals (no medical claims).

### Career
- **CV tailoring agent:** matches CV to a job description, suggests edits, generates interview questions.
- **Learning-path agent:** builds a personalised AI learning roadmap from the user's background.

### Community / local
- **Government services guide (e.g., how to apply for X):** RAG over official documents with step-by-step guidance and sources.
- **Arabic/English bilingual helper** for a specific service or school.

### Developer tools
- **Code review agent** for a repo (read-only, comments on pull requests).
- **Documentation Q&A agent** over a project's docs.

## Make any idea more "agentic"
- Add a **tool** that fetches live data or performs an action (calendar, email draft, spreadsheet, API).
- Add **memory** (preferences, history).
- Add a **plan → act → check** loop with a visible trace.
- Add **human approval** before risky actions.
- Add **evaluation** that shows reliability.

## Ideas to avoid
- Generic "chat with PDF" without a unique angle or tools
- Anything needing sensitive personal data you can't protect
- Anything that makes medical, legal or financial decisions for people
- Projects needing paid infrastructure you can't afford for the demo
- Giant scopes (full SaaS) in 8 days

## Validate your idea in 30 minutes
1. Write the one-sentence pitch: "For **[user]** who **[problem]**, **[app]** is an agent that **[does X using tools Y]**."
2. Talk to 2 potential users; ask what they do today.
3. Write 10 test inputs and the ideal outputs. If you can't, the idea is too vague.
4. List tools/APIs required and check free access.
5. Cut anything not needed for the 2-minute demo.
