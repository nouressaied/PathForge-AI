
from sentence_transformers import SentenceTransformer

print("Chargement du modèle BGE-M3...")

model = SentenceTransformer(
    "BAAI/bge-m3",
    device="cpu"
)

texts = [
    "Data engineer uses Python and SQL.",
    "Machine learning engineer develops AI models.",
    "A nurse provides healthcare to patients."
]

print("Génération des embeddings...")

embeddings = model.encode(
    texts,
    batch_size=2,
    show_progress_bar=True,
    normalize_embeddings=True
)

print("\nTest réussi !")
print("Nombre de textes :", len(texts))
print("Dimension des embeddings :", embeddings.shape[1])
print("Forme de la matrice :", embeddings.shape)
