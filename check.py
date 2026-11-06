from google import genai
from pinecone import Pinecone
from llama_index.core import Settings
import core

core.setup()
client = genai.Client(api_key=core.GOOGLE_API_KEY)

print("Models available to your key (embedding + flash):")
for m in client.models.list():
    actions = getattr(m, "supported_actions", None) or []
    if "embedContent" in actions or "flash" in m.name:
        print("  ", m.name)

vec = Settings.embed_model.get_text_embedding("hello")
print("\nEmbedding OK, dimension:", len(vec))
print("LLM says:", Settings.llm.complete("Reply with the word OK").text)

pc = Pinecone(api_key=core.PINECONE_API_KEY)
print("Pinecone OK, indexes:", pc.list_indexes().names())
print("\nALL GOOD")