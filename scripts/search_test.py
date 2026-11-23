
import argparse

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. CONFIGURATION
# ==========================================

COLLECTION = "pathforge_esco"
MODEL_NAME = "BAAI/bge-m3"

DEFAULT_QUERY = (
    "Which occupations require programming, "
    "Python, SQL and data analysis skills?"
)


# ==========================================
# 2. ARGUMENTS DU TERMINAL
# ==========================================

parser = argparse.ArgumentParser(
    description="PathForge AI - Recherche sémantique ESCO"
)

parser.add_argument(
    "--query",
    type=str,
    default=DEFAULT_QUERY,
    help="Question à rechercher"
)

parser.add_argument(
    "--top-k",
    type=int,
    default=5,
    help="Nombre de résultats à afficher"
)

parser.add_argument(
    "--category",
    type=str,
    default="occupation",
    help="Filtre sur le type de document"
)

args = parser.parse_args()

if not args.query.strip():
    parser.error("La question ne doit pas être vide.")

if args.top_k < 1:
    parser.error("--top-k doit être supérieur ou égal à 1.")


# ==========================================
# 3. CONNEXION À QDRANT
# ==========================================

print("Connexion à Qdrant...")

client = QdrantClient(
    url="http://localhost:6333"
)

print("Collection :", COLLECTION)


# ==========================================
# 4. CHARGEMENT DU MODÈLE
# ==========================================

print("Chargement du modèle BGE-M3...")

model = SentenceTransformer(
    MODEL_NAME,
    device="cpu"
)


# ==========================================
# 5. EMBEDDING DE LA QUESTION
# ==========================================

print("\nQuestion :", args.query)

query_vector = model.encode(
    args.query,
    normalize_embeddings=True
).tolist()


# ==========================================
# 6. RECHERCHE VECTORIELLE
# ==========================================

results = client.search(
    collection_name=COLLECTION,
    query_vector=query_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="type",
                match=models.MatchValue(
                    value=args.category
                )
            )
        ]
    ),
    limit=args.top_k,
    with_payload=True
)


# ==========================================
# 7. AFFICHAGE DES RÉSULTATS
# ==========================================

print(
    f"\n===== TOP {args.top_k} "
    "DES RÉSULTATS ====="
)

if not results:
    print("Aucun résultat trouvé.")

for rank, result in enumerate(results, start=1):

    payload = result.payload or {}

    print(f"\n--- Résultat {rank} ---")

    print("Métier :", payload.get("title"))

    print(
        "Score :",
        round(result.score, 4)
    )

    print("Source :", payload.get("source"))

    print(
        "URI :",
        payload.get("occupation_uri")
    )

    print(
        "Extrait :",
        payload.get("text", "")[:300]
    )

print("\nRecherche terminée.")
