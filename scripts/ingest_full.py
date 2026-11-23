
import json
import uuid
from pathlib import Path

from tqdm import tqdm
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


# ==========================================
# 1. CONFIGURATION
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT / "data" / "processed" / "esco_documents.json"
)

COLLECTION = "pathforge_esco"
MODEL_NAME = "BAAI/bge-m3"

CHUNK_SIZE = 512
OVERLAP = 64
BATCH_SIZE = 8


# ==========================================
# 2. CONNEXION À QDRANT
# ==========================================

print("Connexion à Qdrant...")

client = QdrantClient(
    url="http://localhost:6333",
    timeout=60
)

# Vérifier que Qdrant est accessible
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if COLLECTION not in collection_names:
    raise RuntimeError(
        f"La collection '{COLLECTION}' n'existe pas. "
        "Vérifie Docker et exécute d'abord ingest.py."
    )

info = client.get_collection(COLLECTION)

print("Collection trouvée :", COLLECTION)
print("Points actuels :", info.points_count)


# ==========================================
# 3. CHARGEMENT DES DOCUMENTS
# ==========================================

print("\nChargement des documents ESCO...")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

print("Documents chargés :", len(documents))

# Vérification des champs obligatoires
required_fields = {
    "id",
    "title",
    "text",
    "source",
    "type",
    "essential_skills",
    "optional_skills"
}

for index, doc in enumerate(documents):
    missing = required_fields - set(doc.keys())

    if missing:
        raise ValueError(
            f"Document {index} : champs manquants {missing}"
        )


# ==========================================
# 4. CHARGEMENT DU TOKENIZER
# ==========================================

print("\nChargement du tokenizer BGE-M3...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


# ==========================================
# 5. PRÉPARATION DES CHUNKS
# ==========================================

print("\nPréparation des chunks...")

chunks = []

for doc in tqdm(documents, desc="Découpage ESCO"):

    tokens = tokenizer.encode(
        doc["text"],
        add_special_tokens=False
    )

    start = 0
    chunk_index = 0

    while start < len(tokens):

        part = tokens[start:start + CHUNK_SIZE]

        chunk_text = tokenizer.decode(
            part,
            skip_special_tokens=True
        )

        # Identifiant stable pour éviter les doublons
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                str(doc["id"]) + f"_{chunk_index}"
            )
        )

        chunks.append({
            "id": point_id,
            "text": chunk_text,
            "title": doc["title"],
            "source": doc["source"],
            "type": doc["type"],
            "occupation_uri": str(doc["id"]),
            "chunk_index": chunk_index,
            "essential_skills": doc["essential_skills"],
            "optional_skills": doc["optional_skills"]
        })

        if start + CHUNK_SIZE >= len(tokens):
            break

        start += CHUNK_SIZE - OVERLAP
        chunk_index += 1


print("\nChunks préparés :", len(chunks))


# ==========================================
# 6. IDENTIFIER LES POINTS EXISTANTS
# ==========================================

print("\nVérification des points déjà indexés...")

existing_ids = set()
offset = None

while True:

    points, offset = client.scroll(
        collection_name=COLLECTION,
        limit=256,
        offset=offset,
        with_payload=False,
        with_vectors=False
    )

    for point in points:
        existing_ids.add(str(point.id))

    if offset is None:
        break


print("Points existants :", len(existing_ids))

pending_chunks = [
    chunk
    for chunk in chunks
    if chunk["id"] not in existing_ids
]

print("Chunks restant à indexer :", len(pending_chunks))


# ==========================================
# 7. CHARGEMENT DU MODÈLE BGE-M3
# ==========================================

if pending_chunks:

    print("\nChargement du modèle BGE-M3...")

    model = SentenceTransformer(
        MODEL_NAME,
        device="cpu"
    )

    # ======================================
    # 8. INDEXATION PROGRESSIVE
    # ======================================

    print("\nDébut de l'indexation...")

    for start in tqdm(
        range(0, len(pending_chunks), BATCH_SIZE),
        desc="Indexation Qdrant"
    ):

        batch = pending_chunks[
            start:start + BATCH_SIZE
        ]

        texts = [
            item["text"]
            for item in batch
        ]

        # Génération des embeddings
        vectors = model.encode(
            texts,
            batch_size=4,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        points = []

        for item, vector in zip(batch, vectors):

            payload = {
                key: value
                for key, value in item.items()
                if key != "id"
            }

            points.append(
                models.PointStruct(
                    id=item["id"],
                    vector=vector.tolist(),
                    payload=payload
                )
            )

        # Enregistrement dans Qdrant
        client.upsert(
            collection_name=COLLECTION,
            points=points,
            wait=True
        )

else:
    print("\nTous les chunks sont déjà indexés.")


# ==========================================
# 9. VÉRIFICATION FINALE
# ==========================================

print("\n================================")
print("     INGESTION TERMINÉE")
print("================================")

final_count = client.count(
    collection_name=COLLECTION,
    exact=True
).count

print("Collection :", COLLECTION)
print("Documents ESCO :", len(documents))
print("Chunks préparés :", len(chunks))
print("Points enregistrés :", final_count)

print("\nPathForge AI : indexation terminée !")
