---
title: Deployment Playbook – Take Your AI App Live
doc_type: how_to
last_updated: 2026-11-06
---

# Deployment Playbook

## Principle
**Deploy early (by Day 4–6), then improve.** A live URL is part of a strong submission, and deployment always reveals problems you can't see locally.

## Pre-deployment checklist
- [ ] App runs from a clean clone (`git clone`, install, run)
- [ ] `requirements.txt` / `package.json` is complete
- [ ] All secrets are read from **environment variables**
- [ ] The app listens on host `0.0.0.0` and the platform's `PORT` (where required)
- [ ] No local-only paths (e.g., `C:\Users\...`)
- [ ] No large model downloads at startup if the host has low RAM or slow builds
- [ ] Error handling shows friendly messages (not stack traces)
- [ ] Rate limit / max-steps / timeout set (to protect your API budget)
- [ ] README has the run instructions

## Recipe A – Gradio app on Hugging Face Spaces
1. Create a Hugging Face account → **New Space** → SDK **Gradio** → hardware **CPU basic** (free) → public.
2. Upload (or push by git) `app.py` and `requirements.txt`.
3. Space → **Settings → Variables and secrets** → add `OPENAI_API_KEY` (or your provider's key).
4. Wait for **Building** → **Running**. Open the URL.
Minimal `app.py` pattern:
```python
import os, gradio as gr
def answer(message, history):
    # call your agent here; read keys with os.environ["..."]
    return "Hello from the agent"
gr.ChatInterface(answer).launch()
```
Typical errors: `ModuleNotFoundError` → add package to `requirements.txt`; build error → read build logs; "Runtime error" → check logs and secrets spelling.

## Recipe B – Streamlit app on Streamlit Community Cloud
1. Push `streamlit_app.py` (or `app.py`) and `requirements.txt` to a **GitHub** repo.
2. Go to share.streamlit.io → sign in with GitHub → **New app** → pick repo, branch, main file.
3. **Advanced settings → Secrets**: add keys in TOML, e.g. `OPENAI_API_KEY = "..."`. Read with `st.secrets["OPENAI_API_KEY"]`.
4. Deploy; wait for the build.
Tips: use `@st.cache_resource` for loading vector stores/models once; keep memory low.

## Recipe C – FastAPI back-end on Render
1. Repo contains `main.py` (FastAPI `app`) and `requirements.txt` (include `fastapi`, `uvicorn`).
2. Render → New → Web Service → connect repo.
3. Build: `pip install -r requirements.txt`. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Instance type: Free. Add env vars. Deploy.
5. Test `https://<name>.onrender.com/docs` (FastAPI's auto docs).
6. Remember: free instances **sleep** after 15 min; first request is slow.

## Recipe D – Next.js/React front-end on Vercel (calling your back-end)
1. Push the front-end to GitHub.
2. Vercel → Add New → Project → import repo.
3. Add environment variables (e.g., `NEXT_PUBLIC_API_URL` for your back-end URL). Variables beginning with `NEXT_PUBLIC_` are **visible to the browser**: never put secret keys in them.
4. Deploy. Every `git push` to `main` redeploys.
5. CORS: configure your back-end to allow your Vercel domain.

## Recipe E – No-code deployment
- **Lovable/Base44:** use the Publish/Share button; confirm the public link works logged out; check credits.
- **n8n/Flowise/Make:** activate the workflow/chatflow; use the production webhook URL (not the test URL); embed or share the chat link; keep the instance running (cloud plan or a host).
- Screen-record the workflow canvas as extra evidence for "technical execution".

## Environment variables and secrets (all platforms)
- Local: `.env` file + `python-dotenv` (`load_dotenv()`), never committed.
- Hosts: use the dashboard's **secrets / environment variables** section.
- Rotate keys after the challenge if you shared logs or screen recordings that showed them.

## Persistence (data that survives restarts)
Free hosts often have **ephemeral** disks. Use an external database (Supabase/Postgres, Airtable, Google Sheets) or re-build the vector index at startup from files included in the repo (keep it small).

## Cold starts and wake-up
Free tiers sleep. Visit the app before a demo; mention "may take up to a minute to wake" in the README; keep a backup demo video.

## Monitoring and logs
Read the platform logs after each deploy. Add your own logging for every tool call and error. Keep a screenshot of a successful trace for the demo.

## Budget safety
- Set a **hard spending limit** at your LLM provider where possible.
- Cap tokens per request and requests per user/minute.
- Don't publish a link with an unprotected, unlimited key-backed endpoint; judges' traffic and bots can drain credits.

## After deployment test
Open in an **incognito window** and on a **phone**; run the 5 key demo scenarios; check the logs; share the link with a friend.
