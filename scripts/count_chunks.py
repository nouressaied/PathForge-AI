
import json
from pathlib import Path
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "esco_documents.json"

CHUNK_SIZE = 512
OVERLAP = 64
STEP = CHUNK_SIZE - OVERLAP

print("Chargement des documents ESCO...")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

print("Chargement du tokenizer BGE-M3...")

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")

total_chunks = 0
max_chunks = 0

for document in documents:
    tokens = tokenizer.encode(
        document["text"],
        add_special_tokens=False
    )

    if len(tokens) <= CHUNK_SIZE:
        count = 1
    else:
        count = 1 + (
            (len(tokens) - CHUNK_SIZE + STEP - 1) // STEP
        )

    total_chunks += count
    max_chunks = max(max_chunks, count)

print("\n===== RÉSULTATS =====")
print("Documents :", len(documents))
print("Chunks estimés :", total_chunks)
print("Maximum de chunks par métier :", max_chunks)
print("Dimension des vecteurs : 1024")
