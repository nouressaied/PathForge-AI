
import argparse
import asyncio
import json
import uuid
from pathlib import Path

from qdrant_client import AsyncQdrantClient, models
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from tqdm import tqdm


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "esco_documents_clean.json"

COLLECTION = "pathforge_esco"
MODEL_NAME = "BAAI/bge-m3"
QDRANT_URL = "http://localhost:6333"

CHUNK_SIZE = 512
OVERLAP = 64
VECTOR_SIZE = 1024


def prepare_chunks(documents, tokenizer):
    records = []
    seen_ids = set()

    for doc in tqdm(documents, desc="Chunking ESCO"):
        tokens = tokenizer.encode(
            doc["text"],
            add_special_tokens=False
        )

        start = 0
        index = 0

        while start < len(tokens):
            part = tokens[start:start + CHUNK_SIZE]

            text = tokenizer.decode(
                part,
                skip_special_tokens=True
            )

            # Identique à ingest_full.py
            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    str(doc["id"]) + f"_{index}"
                )
            )

            if point_id in seen_ids:
                raise ValueError(
                    f"Identifiant dupliqué : {point_id}"
                )

            seen_ids.add(point_id)

            records.append({
                "id": point_id,
                "text": text,
                "title": doc["title"],
                "source": doc["source"],
                "type": doc["type"],
                "occupation_uri": str(doc["id"]),
                "chunk_index": index,
                "essential_skills": doc["essential_skills"],
                "optional_skills": doc["optional_skills"]
            })

            if start + CHUNK_SIZE >= len(tokens):
                break

            start += CHUNK_SIZE - OVERLAP
            index += 1

    return records


async def get_existing_ids(client):
    existing_ids = set()
    offset = None

    while True:
        points, offset = await client.scroll(
            collection_name=COLLECTION,
            limit=256,
            offset=offset,
            with_payload=False,
            with_vectors=False
        )

        existing_ids.update(str(point.id) for point in points)

        if offset is None:
            break

    return existing_ids


async def main():
    parser = argparse.ArgumentParser(
        description="PathForge AI - Ingestion ESCO asynchrone"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=64
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Vérifier sans modifier Qdrant"
    )

    args = parser.parse_args()

    if args.batch_size < 1:
        parser.error("--batch-size doit être positif")

    if not DATA_FILE.exists():
        raise FileNotFoundError(DATA_FILE)

    with DATA_FILE.open("r", encoding="utf-8") as f:
        documents = json.load(f)

    print("Documents ESCO :", len(documents))

    required = {
        "id", "title", "text", "source", "type",
        "essential_skills", "optional_skills"
    }

    for i, doc in enumerate(documents):
        missing = required - doc.keys()
        if missing:
            raise ValueError(
                f"Document {i} : champs manquants {missing}"
            )

    print("Chargement du tokenizer BGE-M3...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    records = prepare_chunks(documents, tokenizer)
    print("Chunks préparés :", len(records))

    client = AsyncQdrantClient(
        url=QDRANT_URL,
        timeout=120
    )

    try:
        exists = await client.collection_exists(COLLECTION)

        if not exists:
            if args.dry_run:
                print("Collection absente : création nécessaire.")
                print("Mode simulation : aucune modification.")
                return

            await client.create_collection(
                collection_name=COLLECTION,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=models.Distance.COSINE
                )
            )

        else:
            info = await client.get_collection(COLLECTION)

            # La collection existante doit correspondre
            # au modèle BGE-M3.
            config = info.config.params.vectors

            if not isinstance(config, models.VectorParams):
                raise RuntimeError(
                    "Configuration vectorielle inattendue."
                )

            if (
                config.size != VECTOR_SIZE
                or config.distance != models.Distance.COSINE
            ):
                raise RuntimeError(
                    "Collection incompatible avec BGE-M3."
                )

        existing_ids = await get_existing_ids(client)
        expected_ids = {record["id"] for record in records}

        pending = [
            record for record in records
            if record["id"] not in existing_ids
        ]

        extras = existing_ids - expected_ids

        print("\n===== AUDIT =====")
        print("Points existants :", len(existing_ids))
        print("Chunks attendus :", len(records))
        print("Chunks manquants :", len(pending))
        print("Points supplémentaires :", len(extras))

        if extras:
            raise RuntimeError(
                "Des points supplémentaires sont présents. "
                "Aucune suppression automatique."
            )

        if args.dry_run:
            print("\nMode simulation : aucune modification.")
            return

        if not pending:
            print("\nCorpus déjà entièrement indexé.")
            print("Aucun embedding recalculé.")
        else:
            print("\nChargement du modèle BGE-M3...")
            model = SentenceTransformer(
                MODEL_NAME,
                device="cpu"
            )

            for start in tqdm(
                range(0, len(pending), args.batch_size),
                desc="Ingestion asynchrone"
            ):
                batch = pending[
                    start:start + args.batch_size
                ]

                texts = [item["text"] for item in batch]

                # Calcul CPU dans un thread pour ne pas
                # bloquer la boucle asynchrone.
                vectors = await asyncio.to_thread(
                    model.encode,
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

                await client.upsert(
                    collection_name=COLLECTION,
                    points=points,
                    wait=True
                )

        final_count = (
            await client.count(
                collection_name=COLLECTION,
                exact=True
            )
        ).count

        print("\n===== INGESTION TERMINÉE =====")
        print("Documents :", len(documents))
        print("Chunks attendus :", len(records))
        print("Points Qdrant :", final_count)

        if final_count != len(records):
            raise RuntimeError(
                "Le nombre final de points est incorrect."
            )

        print("Validation réussie !")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
