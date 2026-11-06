---
title: Troubleshooting Common Errors for AI App Builders
doc_type: troubleshooting
last_updated: 2026-11-06
---

# Troubleshooting Guide

When asking for help (WhatsApp group, community, or the assistant), always include: **what you tried, the exact error text, your platform/tool, and the relevant code or settings (with secrets removed).**

## Python / environment
| Error | Likely cause and fix |
|---|---|
| `ModuleNotFoundError: No module named 'x'` | Package not installed → `pip install x` and add to `requirements.txt` |
| `pip` externally-managed-environment | Use a virtual env: `python -m venv .venv`, activate it, then `pip install` |
| Version conflicts | Pin versions in `requirements.txt`; recreate the venv; avoid installing everything you don't use |
| `KeyError: 'OPENAI_API_KEY'` | Env var not set locally (`.env` not loaded) or not added as a secret on the host; check spelling and redeploy/restart |
| `SyntaxError` / indentation | Check Python version and tabs vs spaces |
| Works locally, fails online | Missing dependency, hard-coded path, secret not set on the host, or app not listening on the right port |

## LLM API errors
| Error | Fix |
|---|---|
| 401 Unauthorized / invalid key | Wrong/revoked key, extra spaces or quotes, wrong provider key |
| 429 Too Many Requests / quota exceeded | Rate limit or no credits → slow down, add retry with backoff, check billing/quota, use a smaller/cheaper model |
| 404 model not found | Model name wrong or not available to your account/region |
| Context length exceeded | Send fewer/shorter chunks; summarise history; limit `top_k` |
| Timeout | Reduce output length; add timeouts and retries; stream responses |
| JSON/tool-call parse errors | Use structured output / function calling; validate and retry once with an error message |
| Agent loops forever | Add `MAX_STEPS`, detect repeated tool calls, improve tool descriptions |

## RAG problems
| Symptom | Fix |
|---|---|
| Answers ignore my documents | Check retrieval output first (print retrieved chunks); improve chunking; lower chunk size; increase `top_k`; make the prompt say "answer only from the context" |
| Wrong chunk retrieved | Add titles/headings to chunks; use better embeddings; add metadata filters; try hybrid (keyword + vector) search |
| Hallucinated answer | Add "say you don't know if the context lacks the answer"; show sources; lower temperature |
| Slow startup | Pre-build the index and load it; don't re-embed every start |
| Vector DB empty on host | Disk is ephemeral → rebuild at startup from repo files or use a hosted DB |

## Deployment problems
| Problem | Fix |
|---|---|
| Hugging Face "Build error" | Read build logs; fix `requirements.txt`; check README front-matter (`sdk`, `app_file`) |
| HF Space "Sleeping" | Normal for free hardware; visit to wake it |
| Render "Application failed to respond" / port error | Start command must bind `0.0.0.0:$PORT` |
| Render slow first load | Free instance woke from idle (up to ~1 minute) |
| Streamlit "over resource limits" | Reduce memory (lazy-load, smaller models, cache resources) |
| Vercel function timeout | Move long agent runs to a back-end host; stream; shorten steps |
| CORS error in browser | Allow your front-end origin on the back-end |
| Supabase "project paused" | Restore it in the dashboard; keep it active before judging |
| App works for you, not others | Check it is public, no login needed, no localhost URLs, no hidden dependency on your files |

## No-code builder problems
| Problem | Fix |
|---|---|
| Workflow works in test, not in production | Use the **production** webhook URL, activate the workflow |
| Credentials error | Re-add the API key in the platform's credential manager |
| Credits ran out | Check plan/credits daily; reduce calls; use a cheaper model |
| Output format inconsistent | Add an output-format instruction and an example in the prompt; add a validation node |
| Lovable/Base44 app broken after edits | Revert to a previous version; make smaller prompts; test after each change |

## GitHub problems
See the GitHub guide table (push rejected, conflicts, secrets committed, large files).

## Last-day emergency plan
1. Stop adding features.
2. Deploy the last known working version.
3. Record the demo video (screen recording is fine).
4. Submit the working link + repo + video **at least a few hours** before 11:45 PM GST on 15 Nov.
5. If something breaks, contact the organisers right away (WhatsApp group / connect@decodingdatascience.com).
