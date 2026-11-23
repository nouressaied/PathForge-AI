
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    ROOT / "data" / "processed" / "esco_documents.json"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed" / "esco_documents_clean.json"
)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

unique_documents = {}
duplicate_ids = []

for doc in documents:
    doc_id = str(doc["id"])

    if doc_id in unique_documents:
        duplicate_ids.append(doc_id)

        # Vérifier si les deux documents sont identiques
        if doc != unique_documents[doc_id]:
            print(
                "ATTENTION : contenus différents pour",
                doc_id
            )
    else:
        unique_documents[doc_id] = doc

clean_documents = list(unique_documents.values())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        clean_documents,
        f,
        ensure_ascii=False,
        indent=2
    )

print("\n===== NETTOYAGE ESCO =====")
print("Documents initiaux :", len(documents))
print("Doublons retirés :", len(duplicate_ids))
print("Documents uniques :", len(clean_documents))
print("Fichier créé :", OUTPUT_FILE)

print("\nAucune modification dans Qdrant.")
