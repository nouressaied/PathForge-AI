
import json
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "esco_documents.json"

COLLECTION = "pathforge_esco"
CHUNK_SIZE = 512
OVERLAP = 64

client = QdrantClient(url="http://localhost:6333")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")

expected_ids = set()

for doc in documents:
    tokens = tokenizer.encode(
        doc["text"],
        add_special_tokens=False
    )

    start = 0
    index = 0

    while start < len(tokens):
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                str(doc["id"]) + f"_{index}"
            )
        )

        expected_ids.add(point_id)

        if start + CHUNK_SIZE >= len(tokens):
            break

        start += CHUNK_SIZE - OVERLAP
        index += 1

actual_ids = set()
offset = None

while True:
    points, offset = client.scroll(
        collection_name=COLLECTION,
        limit=256,
        offset=offset,
        with_payload=False,
        with_vectors=False
    )

    actual_ids.update(str(point.id) for point in points)

    if offset is None:
        break

extra_ids = actual_ids - expected_ids
missing_ids = expected_ids - actual_ids

print("\n===== VÉRIFICATION QDRANT =====")
print("Chunks attendus :", len(expected_ids))
print("Points existants :", len(actual_ids))
print("Points supplémentaires :", len(extra_ids))
print("Chunks manquants :", len(missing_ids))

if extra_ids:
    print("\nExemples d'identifiants supplémentaires :")
    for point_id in sorted(extra_ids)[:5]:
        print(point_id)

print("\nAucune suppression effectuée.")
