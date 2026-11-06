import json
import os
import threading
import time
import webbrowser
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pinecone import Pinecone
from pydantic import BaseModel, Field
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.llms import ChatMessage
from llama_index.vector_stores.pinecone import PineconeVectorStore

import core

# ------------------------------------------------------------------
# RAG backend (same brain as before)
# ------------------------------------------------------------------
core.setup()
pc = Pinecone(api_key=core.PINECONE_API_KEY)
vector_store = PineconeVectorStore(pinecone_index=pc.Index(core.INDEX_NAME))
index = VectorStoreIndex.from_vector_store(vector_store)
retriever = index.as_retriever(similarity_top_k=5)

SYSTEM = (
    "You are the official FAQ assistant for the Decoding Data Science challenge. "
    "Answer ONLY using the provided context. If the answer is not in the context, say: "
    "'I couldn't find that in the challenge documents. Please contact the organizers.' "
    "Never invent dates, rules, prizes or links. Be concise, friendly and well formatted."
)
NOT_FOUND = "couldn't find that in the challenge documents"

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# ------------------------------------------------------------------
# Basic abuse protection (your API key is paid, the URL is public)
# ------------------------------------------------------------------
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MIN", "15"))
_hits = defaultdict(deque)
_lock = threading.Lock()


def allowed(ip: str) -> bool:
    now = time.time()
    with _lock:
        q = _hits[ip]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            return False
        q.append(now)
        return True


# ------------------------------------------------------------------
# API
# ------------------------------------------------------------------
app = FastAPI(title="Decoding Data Science FAQ")

# CORS: lets your Vercel frontend call this backend from another domain.
# ALLOWED_ORIGINS is a comma-separated list, e.g. https://dds-faq.vercel.app
# Default "*" is fine for first tests; lock it to your Vercel URL afterwards.
ALLOWED_ORIGINS = [o.strip().rstrip("/") for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    allow_credentials=False,
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=600)
    history: list[dict] = []


def sse(obj: dict) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def source_label(node) -> dict:
    meta = node.metadata or {}
    file_name = meta.get("file_name", "document")
    header = (meta.get("header_path") or "").strip("/")
    title = header.split("/")[-1] if header else ""
    if not title:
        title = Path(file_name).stem.replace("_", " ").replace("-", " ").strip().title()
    return {"file": file_name, "title": title}


@app.get("/")
def home():
    page = STATIC_DIR / "index.html"
    if page.exists():
        return FileResponse(page)
    return {"status": "DDS FAQ backend is running"}


@app.get("/config.js")
def config_js():
    # When this server serves the page itself (local run), the API is on the same origin.
    return Response("window.API_BASE = '';", media_type="application/javascript")


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/api/chat")
def chat(req: ChatRequest, request: Request):
    fwd = request.headers.get("x-forwarded-for", "")
    ip = fwd.split(",")[0].strip() or (request.client.host if request.client else "unknown")
    if not allowed(ip):
        raise HTTPException(status_code=429, detail="Too many questions. Please wait a minute.")

    message = req.message.strip()
    prior = []
    for m in req.history[-6:]:
        if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str):
            prior.append({"role": m["role"], "content": m["content"][:2000]})

    def generate():
        full = ""
        try:
            nodes = retriever.retrieve(message)
            context = "\n\n---\n\n".join(
                f"[{i+1}] ({n.metadata.get('file_name', 'doc')})\n{n.get_content(metadata_mode='none')}"
                for i, n in enumerate(nodes)
            )
            msgs = [ChatMessage(role="system", content=SYSTEM)]
            for m in prior:
                msgs.append(ChatMessage(role=m["role"], content=m["content"]))
            msgs.append(ChatMessage(role="user", content=f"Context:\n{context}\n\nQuestion: {message}"))

            for chunk in Settings.llm.stream_chat(msgs):
                delta = chunk.delta or ""
                if delta:
                    full += delta
                    yield sse({"t": "delta", "v": delta})

            if NOT_FOUND not in full.lower():
                seen, sources = set(), []
                for n in nodes:
                    s = source_label(n)
                    key = (s["file"], s["title"])
                    if key not in seen:
                        seen.add(key)
                        sources.append(s)
                if sources:
                    yield sse({"t": "sources", "v": sources[:3]})
        except Exception as e:
            print("ERROR in /api/chat:", repr(e))
            busy = "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)
            yield sse({
                "t": "error",
                "v": "The assistant is busy right now. Please try again in a minute."
                if busy else "Something went wrong. Please try again.",
            })
        yield sse({"t": "done"})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    if "PORT" not in os.environ:
        threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        print(f"\n>>> Open this in your browser: http://localhost:{port}\n")
    uvicorn.run(app, host="0.0.0.0", port=port)