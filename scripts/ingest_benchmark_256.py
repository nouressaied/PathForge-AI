
import asyncio
import json
import uuid
from pathlib import Path

from tqdm import tqdm
from qdrant_client import AsyncQdrantClient, models
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT / "data" / "processed"
    / "esco_documents_clean.json"
)

COLLECTION = "pathforge_esco_256"
MODEL_NAME = "BAAI/bge-m3"

CHUNK_SIZE = 256
OVERLAP = 32
BATCH_SIZE = 64
EMBEDDING_BATCH_SIZE = 4


def prepare_chunks(documents, tokenizer):
    records = []

    for doc in tqdm(documents, desc="Chunking 256"):
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

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"benchmark256:{doc['id']}:{index}"
                )
            )

            records.append({
                "id": point_id,
                "text": text,
                "title": doc["title"],
                "source": doc["source"],
                "type": doc["type"],
                "occupation_uri": str(doc["id"]),
                "chunk_index": index
            })

            if start + CHUNK_SIZE >= len(tokens):
                break

            start += CHUNK_SIZE - OVERLAP
            index += 1

    return records


async def get_existing_ids(client):
    existing = set()
    offset = None

    while True:
        points, offset = await client.scroll(
            collection_name=COLLECTION,
            limit=256,
            offset=offset,
            with_payload=False,
            with_vectors=False
        )

        existing.update(str(p.id) for p in points)

        if offset is None:
            break

    return existing


async def main():
    print("Chargement du dataset ESCO...")

    with DATA_FILE.open("r", encoding="utf-8") as f:
        documents = json.load(f)

    print("Documents :", len(documents))

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    records = prepare_chunks(documents, tokenizer)

    print("Chunks préparés :", len(records))

    client = AsyncQdrantClient(
        url="http://localhost:6333",
        timeout=120
    )

    try:
        if not await client.collection_exists(COLLECTION):
            await client.create_collection(
                collection_name=COLLECTION,
                vectors_config=models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE
                )
            )

        existing_ids = await get_existing_ids(client)

        pending = [
            record for record in records
            if record["id"] not in existing_ids
        ]

        print("Points existants :", len(existing_ids))
        print("Chunks à indexer :", len(pending))

        if pending:
            model = SentenceTransformer(
                MODEL_NAME,
                device="cpu"
            )

            for start in tqdm(
                range(0, len(pending), BATCH_SIZE),
                desc="Indexation 256"
            ):
                batch = pending[
                    start:start + BATCH_SIZE
                ]

                vectors = await asyncio.to_thread(
                    model.encode,
                    [item["text"] for item in batch],
                    batch_size=EMBEDDING_BATCH_SIZE,
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

        count = (
            await client.count(
                collection_name=COLLECTION,
                exact=True
            )
        ).count

        print("\n===== BENCHMARK 256 =====")
        print("Documents :", len(documents))
        print("Chunks attendus :", len(records))
        print("Points Qdrant :", count)

        if count != len(records):
            raise RuntimeError(
                "Indexation incomplète ou points supplémentaires."
            )

        print("Indexation 256 validée !")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
