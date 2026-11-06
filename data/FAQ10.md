---
title: Tools and Platforms Guide – Models, Frameworks, No-Code Builders, Coding Assistants
doc_type: tools_guide
last_updated: 2026-11-06
---

# Tools and Platforms Guide

Pricing and free limits change often. Treat numbers here as general guidance and check each provider's current pricing page before relying on a limit.

## 1. LLM (model) providers
| Provider | Notes |
|---|---|
| OpenAI API | Popular, strong tool/function-calling support, paid usage (no permanent free API tier) |
| Anthropic (Claude API) | Strong at long documents, coding and tool use, paid usage |
| Google Gemini API (Google AI Studio) | Has historically offered a free tier with rate limits; good for prototypes |
| Amazon Bedrock | Access to multiple models through AWS; the challenge names it explicitly; requires an AWS account |
| Groq, OpenRouter, Together, Hugging Face Inference | Hosted open models; some free or low-cost options with limits |
| Ollama / LM Studio (local) | Run open models on your own computer for free; needs a decent laptop; not directly hostable on free cloud tiers |
**Advice:** pick one provider and one model for the whole challenge. Avoid switching late. Put the model name in an environment variable so you can change it easily. Check rate limits early so you don't hit them during the final demo.

## 2. Coding assistants (Code-First path)
Named by the organisers: **Cursor, Claude Code, Codex** (also OpenAI APIs, Amazon Bedrock).
How to use them well:
- Give them your plan (the Project Idea template) and the stack.
- Ask for small, testable steps ("create the retrieval function and a test").
- Always read and run the code; never paste secrets into prompts.
- Ask the assistant to explain errors, write README text and add tests.
- **JetBrains** IDEs (PyCharm, WebStorm, etc.) are the challenge's licence sponsor. The licence is a prize, not a requirement.

## 3. Agent and RAG frameworks (code)
- **LangChain / LangGraph:** big ecosystem, graph-based agent control.
- **LlamaIndex:** strong for RAG and document pipelines.
- **CrewAI, AutoGen:** multi-agent setups.
- **OpenAI Agents SDK, Google ADK, Pydantic AI, smolagents:** lighter agent frameworks.
- **Plain Python + function calling:** simplest and often the most reliable for a challenge.

## 4. No-code / low-code builders (named by the organisers)
| Tool | Best for |
|---|---|
| **Lovable** | Generate a full web app/UI from a prompt |
| **Base44** | Build apps with built-in backend/data from prompts |
| **n8n** | Workflow automation and AI agent flows; self-host or cloud |
| **Flowise** | Visual drag-and-drop LLM/agent/RAG flows |
| **Make** | App-to-app automations with AI steps |
| Others commonly used: Zapier, Voiceflow, Bubble, Langflow | Chatbots, automations, full no-code web apps |
**Advice for no-code builders:** keep the workflow small; test each node; store keys in the platform's credentials manager; publish early; make a screen recording of the workflow plus the final app (judges also assess execution quality).

## 5. UI options (code)
- **Gradio:** fastest way to give a Python function a web UI; ideal for Hugging Face Spaces.
- **Streamlit:** Python dashboards and chat apps; easy deploy via Streamlit Community Cloud.
- **FastAPI + HTML/JS** or **Next.js/React:** more control and a polished feel; deploy on Render/Vercel/Railway.

## 6. Data and vector stores
- **Chroma, FAISS:** local, free, easy.
- **Qdrant, Pinecone, Weaviate:** hosted vector DBs (free tiers exist; check limits).
- **Supabase (Postgres + pgvector):** database + auth + storage in one.
- **SQLite:** simplest relational store; note that free cloud hosts often have **ephemeral disks**, so data may vanish on restart.
- **Google Sheets / Airtable:** easy data store for no-code projects.

## 7. Helpful extras
- **Google Colab / Jupyter:** prototype quickly.
- **Postman or curl:** test APIs.
- **GitHub Codespaces / VS Code:** cloud or local editor.
- **Loom / OBS:** screen recording for the demo.
- **Canva:** thumbnail or poster for the LinkedIn post.
- **LangSmith, Langfuse, Phoenix:** tracing and evaluation for agents (optional).

## 8. Choosing quickly (decision guide)
- Need a chat UI over documents in 1 day → Gradio/Streamlit + Chroma + one LLM API.
- Need automation across Gmail/Sheets/Slack → n8n or Make.
- Need a polished full web app and no coding → Lovable or Base44 (+ n8n for agent logic).
- Need an API plus a custom UI → FastAPI + Next.js, deploy on Render + Vercel.
