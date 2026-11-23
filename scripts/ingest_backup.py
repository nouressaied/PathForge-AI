
import json
import uuid
from pathlib import Path

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "esco_documents.json"

COLLECTION = "pathforge_esco"
MODEL_NAME = "BAAI/bge-m3"
CHUNK_SIZE = 512
OVERLAP = 64
BATCH_SIZE = 4

# 1. Charger les documents ESCO
with open(DATA_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

print(f"Documents chargés : {len(documents)}")

# 2. Charger le modèle et son tokenizer
print("Chargement de BGE-M3...")
model = SentenceTransformer(MODEL_NAME, device="cpu")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# 3. Découper les textes en chunks
def split_text(text):
    tokens = tokenizer.encode(
        text,
        add_special_tokens=False
    )

    chunks = []
    step = CHUNK_SIZE - OVERLAP

    for start in range(0, len(tokens), step):
        part = tokens[start:start + CHUNK_SIZE]

        if not part:
            break

        chunks.append(
            tokenizer.decode(
                part,
                skip_special_tokens=True
            )
        )

        if start + CHUNK_SIZE >= len(tokens):
            break

    return chunks


records = []

for doc in documents:
    chunks = split_text(doc["text"])

    for index, chunk in enumerate(chunks):
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{doc['id']}:{index}"
            )
        )

        records.append({
            "id": point_id,
            "text": chunk,
            "title": doc["title"],
            "source": doc["source"],
            "type": doc["type"],
            "occupation_uri": doc["id"],
            "chunk_index": index,
            "essential_skills": doc["essential_skills"],
            "optional_skills": doc["optional_skills"],
        })

print(f"Chunks préparés : {len(records)}")

# 4. Connexion à Qdrant
client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(
            size=1024,
            distance=models.Distance.COSINE
        )
    )

# 5. Générer les embeddings et les indexer
print("Début de l'indexation...")

for start in range(0, len(records), BATCH_SIZE):
    batch = records[start:start + BATCH_SIZE]

    embeddings = model.encode(
        [item["text"] for item in batch],
        batch_size=BATCH_SIZE,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    points = []

    for item, vector in zip(batch, embeddings):
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

    client.upsert(
        collection_name=COLLECTION,
        points=points,
        wait=True
    )

    print(
        f"Indexés : {min(start + BATCH_SIZE, len(records))}"
        f"/{len(records)}"
    )

# 6. Vérifier le nombre de points
count = client.count(
    collection_name=COLLECTION,
    exact=True
).count

print("\nIngestion terminée !")
print("Collection :", COLLECTION)
print("Points enregistrés :", count)
