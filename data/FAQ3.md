---
title: What Is Agentic AI? A Detailed Beginner-to-Builder Guide
doc_type: concept_guide
last_updated: 2026-11-06
---

# What Is Agentic AI?

## One-sentence definition
**Agentic AI** is AI that doesn't just answer a prompt: it pursues a goal by **planning, choosing and calling tools, observing results, and adjusting**, with limited human supervision, until the task is done.

## Chatbot vs. agent (the core difference)
| | Plain chatbot / LLM | AI agent (agentic) |
|---|---|---|
| Input | A question | A goal ("book me the cheapest flight and add it to my calendar") |
| Output | Text answer | Actions + results (API calls, files, emails, database updates) |
| Steps | One response | Multi-step loop |
| Tools | None | Search, code execution, databases, APIs, other agents |
| State | Only the chat window | Memory, task state, logs |
| Failure mode | Wrong answer | Wrong **action** (higher stakes → needs guardrails) |

A useful rule: **if your app only generates text from a prompt, it's an LLM app. If it decides what to do next and does it, it's agentic.**

## The agent loop
1. **Perceive:** read the user's goal and the current state (messages, files, tool results).
2. **Plan / reason:** decide the next step (or break the goal into sub-tasks).
3. **Act:** call a tool (search, calculator, API, database query, code interpreter).
4. **Observe:** read the tool result.
5. **Reflect / decide:** is the goal met? If not, go back to step 2.
6. **Respond:** give the user the final result (and what the agent did).
This is often called **ReAct** (Reason + Act) or a tool-use loop.

## Building blocks of an agent
1. **LLM (the "brain"):** decides, writes, reasons. Examples of model families: GPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama/Mistral/Qwen (open models), Amazon Bedrock hosted models.
2. **System prompt / instructions:** the agent's role, rules, tone, safety limits and when to use which tool.
3. **Tools (a.k.a. function calling):** functions the model may call: web search, SQL query, send email, create calendar event, read a PDF, call a REST API. The model outputs a structured request (name + arguments); your code runs it and returns the result.
4. **Memory:**
   - *Short-term:* conversation context.
   - *Long-term:* stored facts/preferences in a database or vector store.
   - *Working state:* the task's plan and progress.
5. **Knowledge / retrieval (RAG):** the agent looks up your documents before answering (see below).
6. **Orchestration:** the code or framework that runs the loop, handles retries, limits steps and logs everything.
7. **Guardrails:** input/output validation, permission limits, human approval for risky actions, cost and step limits.
8. **Evaluation and observability:** test cases, logs, traces, so you can see why the agent did what it did.

## RAG (Retrieval-Augmented Generation) in plain words
RAG = give the model **your own documents** at answer time.
1. Split documents into chunks.
2. Turn each chunk into an **embedding** (a vector of numbers capturing meaning).
3. Store them in a **vector database** (e.g. Chroma, FAISS, Qdrant, Pinecone, pgvector).
4. When the user asks a question, embed the question, retrieve the most similar chunks.
5. Put the chunks into the prompt and tell the model to answer **only from them** and cite the source.
RAG reduces hallucination and lets the app use private or up-to-date information. An agent can treat RAG as **one of its tools** ("search_knowledge_base").

## Levels of "agentic-ness"
1. **Prompted LLM:** single call.
2. **Workflow / chain:** fixed steps (summarise → classify → email). Predictable, often enough.
3. **Tool-using agent:** the model chooses tools in a loop.
4. **Multi-agent system:** several specialised agents (researcher, writer, reviewer) coordinated by an orchestrator.
5. **Autonomous long-running agents:** run for hours with minimal supervision (needs strong guardrails).
**Practical advice for an 8-day challenge:** aim for level 2–3. A reliable tool-using agent with 2–4 well-defined tools beats a flaky multi-agent demo.

## Real-world examples
- **Customer support agent:** reads the question, searches the help-centre (RAG), checks order status (API), drafts a reply, escalates to a human if unsure.
- **Research assistant:** searches the web, reads pages, extracts facts, writes a cited report.
- **Data analyst agent:** takes a question, writes SQL/Python, runs it, charts the result, explains it.
- **Recruiting assistant:** parses CVs, scores against a job description, drafts interview questions, books slots.
- **Personal finance helper:** reads a bank CSV, categorises spending, flags anomalies (privacy-sensitive, so keep data local).
- **Study buddy:** quizzes you from your notes (RAG), tracks weak topics (memory), schedules revision.

## Key concepts and vocabulary
- **Prompt engineering:** writing clear instructions and examples.
- **Function calling / tool use:** structured model output to invoke code.
- **MCP (Model Context Protocol):** an open standard for connecting AI apps to tools and data sources through "MCP servers". Useful if you want to plug tools in without custom glue code.
- **Agent frameworks:** LangChain/LangGraph, LlamaIndex, CrewAI, AutoGen, OpenAI Agents SDK, Google ADK, Pydantic AI, Smolagents, Amazon Bedrock Agents. Frameworks help but are optional; a plain Python loop with function calling is perfectly valid and easier to debug.
- **Low-code agent builders:** n8n, Flowise, Make, Langflow.
- **Hallucination:** confident but wrong output.
- **Prompt injection:** malicious text (in a web page, document or user message) that tries to hijack the agent's instructions. Real risk for agents that read external content and have powerful tools.
- **Human-in-the-loop:** requiring approval before high-impact actions (sending money, emails, deleting data).
- **Context window:** how much text the model can consider at once.
- **Latency and cost:** every loop iteration costs tokens and time; set a max-steps limit.

## Risks and how to handle them
| Risk | Mitigation |
|---|---|
| Hallucinated facts | RAG + "answer only from sources" + citations + "I don't know" fallback |
| Wrong or destructive actions | Least-privilege tools, confirmation step, dry-run mode, read-only by default |
| Prompt injection | Treat retrieved/external text as **data not instructions**; restrict tools; validate tool arguments |
| Runaway loops / cost | Max steps, timeouts, token budget, rate limits |
| Data leakage | Never put secrets or private data into prompts or logs; mask personal data |
| Bias / unfair outputs | Test on varied inputs; state limitations |
| Over-trust by users | Show sources, label AI output, keep human review for critical decisions |

## How to know your project is truly "agentic" (judge-friendly checklist)
- [ ] The system decides **which step or tool** to use next (not a hard-coded single path only)
- [ ] It uses at least one **real tool** (API, database, search, code, file)
- [ ] It maintains **state or memory** across steps
- [ ] It has **guardrails** and fails gracefully
- [ ] You can show a **trace/log** of its reasoning and actions in the demo
- [ ] It solves a real problem for a named user

## Common beginner mistakes
- Building a "chatbot with a nicer UI" and calling it an agent
- Too many tools or agents with no testing
- No evaluation: you never tested 10 realistic inputs
- Hard-coding API keys in the repository
- Not deploying until the last day
