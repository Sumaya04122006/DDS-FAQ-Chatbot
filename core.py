import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "dsc-faq")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.6-flash")
EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")


def setup():
    if not GOOGLE_API_KEY or not PINECONE_API_KEY:
        raise RuntimeError("Missing GOOGLE_API_KEY or PINECONE_API_KEY (check .env / Render env vars)")
    Settings.embed_model = GoogleGenAIEmbedding(model_name=EMBED_MODEL, api_key=GOOGLE_API_KEY)
    Settings.llm = GoogleGenAI(model=LLM_MODEL, api_key=GOOGLE_API_KEY)