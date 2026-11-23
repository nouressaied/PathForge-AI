
import json
from collections import defaultdict
from pathlib import Path

from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT / "data" / "processed" / "esco_documents.json"
)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")

CHUNK_SIZE = 512
OVERLAP = 64

# Identifier les documents partageant un ID
documents_by_id = defaultdict(list)

for doc in documents:
    documents_by_id[str(doc["id"])].append(doc["title"])

duplicates = {
    doc_id: titles
    for doc_id, titles in documents_by_id.items()
    if len(titles) > 1
}

print("===== VÉRIFICATION DES IDs ESCO =====")
print("Documents :", len(documents))
print("IDs uniques :", len(documents_by_id))
print("IDs répétés :", len(duplicates))

for doc_id, titles in duplicates.items():
    print("\nID :", doc_id)
    print("Métiers :", titles)

# Vérifier les identifiants des chunks
chunk_ids = defaultdict(list)

for doc in documents:
    tokens = tokenizer.encode(
        doc["text"],
        add_special_tokens=False
    )

    start = 0
    index = 0

    while start < len(tokens):
        chunk_key = (str(doc["id"]), index)

        chunk_ids[chunk_key].append(doc["title"])

        if start + CHUNK_SIZE >= len(tokens):
            break

        start += CHUNK_SIZE - OVERLAP
        index += 1

collisions = {
    key: titles
    for key, titles in chunk_ids.items()
    if len(titles) > 1
}

print("\n===== VÉRIFICATION DES CHUNKS =====")
print(
    "Identifiants uniques :",
    len(chunk_ids)
)
print(
    "Collisions :",
    len(collisions)
)

for key, titles in collisions.items():
    print("\nClé :", key)
    print("Métiers concernés :", titles)

print("\nAucune donnée modifiée.")
