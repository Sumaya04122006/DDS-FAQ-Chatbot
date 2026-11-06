import os
import time
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from llama_index.vector_stores.pinecone import PineconeVectorStore
import core

core.setup()

# Free Gemini tier = 100 embed requests/minute. Stay under it.
# On a paid key you can set EMBED_PAUSE=0 and EMBED_BATCH=200 in .env
BATCH = int(os.getenv("EMBED_BATCH", "80"))
PAUSE = int(os.getenv("EMBED_PAUSE", "65"))

# ---- 1. Check the data folder BEFORE touching Pinecone ----
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
has_md = os.path.isdir(DATA_DIR) and any(
    f.lower().endswith(".md") for _, _, files in os.walk(DATA_DIR) for f in files
)
if not has_md:
    raise SystemExit(f"No .md files found in {DATA_DIR}. Put your markdown files there first.")

# ---- 2. Load and chunk the markdown files ----
docs = SimpleDirectoryReader(DATA_DIR, required_exts=[".md"], recursive=True).load_data()
print(f"Loaded {len(docs)} documents")

nodes = MarkdownNodeParser().get_nodes_from_documents(docs)
nodes = SentenceSplitter(chunk_size=800, chunk_overlap=100).get_nodes_from_documents(nodes)
print(f"Created {len(nodes)} chunks")

# ---- 3. Connect to Pinecone ----
pc = Pinecone(api_key=core.PINECONE_API_KEY)

dim = len(Settings.embed_model.get_text_embedding("dimension probe"))
print("Embedding dimension:", dim)

# Fresh index each run so re-ingesting never creates duplicates
if core.INDEX_NAME in pc.list_indexes().names():
    print("Deleting old index...")
    pc.delete_index(core.INDEX_NAME)
    time.sleep(5)

pc.create_index(
    name=core.INDEX_NAME,
    dimension=dim,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)
while not pc.describe_index(core.INDEX_NAME).status["ready"]:
    time.sleep(2)
print("Pinecone index ready.")

# ---- 4. Embed + upload in rate-limit-friendly batches ----
vector_store = PineconeVectorStore(pinecone_index=pc.Index(core.INDEX_NAME))
index = VectorStoreIndex.from_vector_store(vector_store)

total = len(nodes)
batches = [nodes[i:i + BATCH] for i in range(0, total, BATCH)]

for n, batch in enumerate(batches, start=1):
    for attempt in range(1, 5):
        try:
            index.insert_nodes(batch)
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"  Rate limited, waiting {PAUSE}s (attempt {attempt}/4)...")
                time.sleep(PAUSE)
            else:
                raise
    else:
        raise SystemExit("Gave up after 4 rate-limit retries. Wait a few minutes and run again.")

    done = min(n * BATCH, total)
    print(f"Batch {n}/{len(batches)} uploaded ({done}/{total} chunks)")
    if n < len(batches) and PAUSE > 0:
        print(f"  Pausing {PAUSE}s to respect the free-tier limit...")
        time.sleep(PAUSE)

print("DONE. Vectors in Pinecone.")