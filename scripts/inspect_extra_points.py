
import json
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "esco_documents.json"

client = QdrantClient(url="http://localhost:6333")
collection = "pathforge_esco"

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

        if start + 512 >= len(tokens):
            break

        start += 448
        index += 1

actual_ids = set()
offset = None

while True:
    points, offset = client.scroll(
        collection_name=collection,
        limit=256,
        offset=offset,
        with_payload=False,
        with_vectors=False
    )

    actual_ids.update(str(p.id) for p in points)

    if offset is None:
        break

extra_ids = sorted(actual_ids - expected_ids)

print("Points supplémentaires :", len(extra_ids))

if extra_ids:
    points = client.retrieve(
        collection_name=collection,
        ids=extra_ids[:5],
        with_payload=True,
        with_vectors=False
    )

    for point in points:
        payload = point.payload or {}

        print("\n-----------------------")
        print("ID :", point.id)
        print("Métier :", payload.get("title"))
        print("URI :", payload.get("occupation_uri"))
        print("Chunk :", payload.get("chunk_index"))
        print("Source :", payload.get("source"))
        print("Extrait :", payload.get("text", "")[:150])

print("\nAucune donnée supprimée.")
