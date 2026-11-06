---
title: GitHub Guide for Challenge Participants – From Zero to Submission
doc_type: how_to
last_updated: 2026-11-06
---

# GitHub Guide (for the challenge)

## Why GitHub?
- Judges and recruiters look at your **repository**.
- Most hosts (Render, Vercel, Streamlit Community Cloud, Railway) deploy **directly from GitHub**.
- It gives you version history, backup and collaboration.

## Core words
- **Git:** version control tool on your computer.
- **GitHub:** website that hosts Git repositories.
- **Repository (repo):** a project folder tracked by Git.
- **Commit:** a saved snapshot with a message.
- **Branch:** a parallel line of work (`main` is the default).
- **Push / Pull:** send/get commits to/from GitHub.
- **Clone:** download a repo.
- **Pull request (PR):** propose merging a branch.

## Setup (once)
1. Create an account at github.com.
2. Install Git (git-scm.com) or use **GitHub Desktop** (point-and-click, great for beginners).
3. Configure identity:
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
4. Sign in from the command line using the GitHub CLI (`gh auth login`) or a personal access token, or use GitHub Desktop/VS Code sign-in. (Password login for Git over HTTPS is not supported; use a token, SSH key or the CLI.)

## Create and push your first repo (command line)
```
mkdir my-agent-app && cd my-agent-app
git init
# add your files: app.py, requirements.txt, README.md, .gitignore
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/my-agent-app.git
git push -u origin main
```
Or create the repo on github.com first (New repository → add README and a Python `.gitignore`), then `git clone` it.

## Everyday workflow
```
git status                 # what changed?
git add .                  # stage changes
git commit -m "Add retrieval tool"
git push                   # upload to GitHub
git pull                   # get latest changes (do before you start working)
```
Commit **small and often** with clear messages. Push at least every day: it's your backup and your proof of progress.

## Branches (simple use)
```
git checkout -b feature/ui     # create + switch
git push -u origin feature/ui
# merge on GitHub via a pull request, or locally:
git checkout main && git merge feature/ui
```
If you are working alone, working on `main` is fine. Use branches for risky experiments.

## .gitignore: files you must NOT commit
Create `.gitignore` containing at least:
```
.env
.env.*
*.key
__pycache__/
.venv/
venv/
node_modules/
.DS_Store
*.sqlite
chroma_db/
```
Commit a **`.env.example`** with variable names only (no real values), e.g. `OPENAI_API_KEY=your_key_here`.

## NEVER commit secrets (very important)
- API keys, tokens, database passwords must **never** be in the repo. Bots scan GitHub within minutes and abuse leaked keys.
- If you accidentally commit a key: **revoke/rotate the key immediately** at the provider. Deleting the file or a later commit does **not** remove it from history.
- Store secrets as **environment variables** locally (`.env` + `python-dotenv`) and as **secrets** on the host (HF Space secrets, Render env vars, Vercel env vars, Streamlit secrets, GitHub Actions secrets).

## A good README (judges read this)
Include:
1. Project name + one-line pitch
2. Problem and target user
3. **Live demo link** and demo video link
4. Screenshot/GIF
5. Features (what makes it agentic: tools, memory, guardrails)
6. Tech stack and architecture diagram (a simple image is fine)
7. How to run locally (step-by-step, with `.env.example`)
8. Limitations and future work
9. Credits and licence
Template:
```
# Project Name
One-line description.
**Demo:** <link> · **Video:** <link>
## Problem
## Solution
## How it works (architecture)
## Tech stack
## Run locally
1. git clone ...
2. python -m venv .venv && source .venv/bin/activate
3. pip install -r requirements.txt
4. cp .env.example .env  # add your keys
5. python app.py
## Limitations
## Roadmap
```

## requirements.txt (Python)
Freeze your dependencies so hosts can build your app:
```
pip freeze > requirements.txt
```
Better: list only the packages you actually import, with versions where possible. A bloated or missing `requirements.txt` is the #1 cause of failed deployments.

## Public vs private repos
- **Public** is the easiest for judges and for free hosting (Streamlit free route expects public repos).
- If private, add judges/organisers as collaborators or follow the submission instructions. Check what the final checkpoint asks for.

## GitHub features worth knowing
- **GitHub Codespaces:** a cloud VS Code environment; handy on a weak laptop.
- **GitHub Pages:** free hosting for static sites (Settings → Pages).
- **GitHub Actions:** automate tests/deployments (optional).
- **Releases/tags:** mark your final submitted version, e.g. `v1.0-submission`.
- **Issues/Projects:** a simple task board.

## Common Git problems
| Problem | Fix |
|---|---|
| `rejected: non-fast-forward` on push | `git pull --rebase` then `git push` |
| Merge conflict | Open the conflicted file, keep the right lines, remove `<<<<<<<` markers, `git add`, `git commit` |
| Committed a big file / secret | Remove it, add to `.gitignore`, **rotate the secret**; for history cleanup use `git filter-repo` or BFG (advanced) |
| "Permission denied (publickey)" | Set up an SSH key or use HTTPS with a token/CLI login |
| Wrong branch name | `git branch -M main` |
| File over 100 MB rejected | Don't commit models/datasets; use Git LFS or external storage |

## Freeze before submission
Tag the final commit, confirm the README renders, confirm the live link works from an incognito window, and confirm no secrets are in the repo.
