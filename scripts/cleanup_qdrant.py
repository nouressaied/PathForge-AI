
import json
import uuid
from pathlib import Path

from qdrant_client import QdrantClient, models
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT / "data" / "processed" / "esco_documents_clean.json"
)

COLLECTION = "pathforge_esco"
MODEL_NAME = "BAAI/bge-m3"

CHUNK_SIZE = 512
OVERLAP = 64

client = QdrantClient(url="http://localhost:6333")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

expected_ids = set()
expected_uris = set()

for doc in documents:
    occupation_uri = str(doc["id"])
    expected_uris.add(occupation_uri)

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
                occupation_uri + f"_{index}"
            )
        )

        expected_ids.add(point_id)

        if start + CHUNK_SIZE >= len(tokens):
            break

        start += CHUNK_SIZE - OVERLAP
        index += 1

actual_points = []
offset = None

while True:
    points, offset = client.scroll(
        collection_name=COLLECTION,
        limit=256,
        offset=offset,
        with_payload=True,
        with_vectors=False
    )

    actual_points.extend(points)

    if offset is None:
        break

actual_ids = {str(p.id) for p in actual_points}

extra_points = [
    p for p in actual_points
    if str(p.id) not in expected_ids
]

missing_ids = expected_ids - actual_ids

# Vérifier que chaque point supplémentaire
# appartient bien au corpus ESCO propre.
safe_to_delete = (
    len(missing_ids) == 0
    and all(
        (p.payload or {}).get("occupation_uri")
        in expected_uris
        for p in extra_points
    )
)

print("\n===== AUDIT QDRANT =====")
print("Documents propres :", len(documents))
print("Chunks attendus :", len(expected_ids))
print("Points présents :", len(actual_ids))
print("Points supplémentaires :", len(extra_points))
print("Chunks manquants :", len(missing_ids))
print("Points supplémentaires reconnus :", safe_to_delete)

if not safe_to_delete:
    print("\nNettoyage annulé : vérification non validée.")

elif not extra_points:
    print("\nAucun point supplémentaire à supprimer.")

else:
    print("\nExemples de points supplémentaires :")

    for point in extra_points[:5]:
        payload = point.payload or {}
        print(
            point.id,
            "|",
            payload.get("title")
        )

    confirmation = input(
        "\nPour supprimer uniquement ces anciens points, "
        "tape SUPPRIMER : "
    )

    if confirmation == "SUPPRIMER":
        ids_to_delete = [p.id for p in extra_points]

        client.delete(
            collection_name=COLLECTION,
            points_selector=models.PointIdsList(
                points=ids_to_delete
            ),
            wait=True
        )

        final_count = client.count(
            collection_name=COLLECTION,
            exact=True
        ).count

        print("\nNettoyage terminé.")
        print("Points restants :", final_count)

    else:
        print("\nSuppression annulée.")
