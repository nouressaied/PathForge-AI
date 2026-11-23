
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "esco"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# Lire les métiers et leurs relations
occupations = pd.read_csv(RAW / "occupations_en.csv")
relations = pd.read_csv(
    RAW / "occupationSkillRelations_en.csv"
)

# Premier échantillon reproductible

# Utiliser tous les métiers ESCO
sample = occupations.copy()

# Garder uniquement les relations des métiers choisis
selected_relations = relations[
    relations["occupationUri"].isin(sample["conceptUri"])
]

documents = []

for _, occupation in sample.iterrows():
    uri = occupation["conceptUri"]
    label = str(occupation["preferredLabel"])
    description = occupation["description"]

    if pd.isna(description):
        description = ""

    skills = selected_relations[
        selected_relations["occupationUri"] == uri
    ]

    essential = skills[
        skills["relationType"] == "essential"
    ]["skillLabel"].dropna().unique().tolist()

    optional = skills[
        skills["relationType"] == "optional"
    ]["skillLabel"].dropna().unique().tolist()

    text = (
        f"Occupation: {label}\n"
        f"Description: {description}\n"
        f"Essential skills: {', '.join(essential)}\n"
        f"Optional skills: {', '.join(optional)}"
    )

    documents.append({
        "id": uri,
        "title": label,
        "text": text,
        "source": "ESCO v1.2.1",
        "type": "occupation",
        "essential_skills": essential,
        "optional_skills": optional
    })

output_file = OUT / "esco_documents.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=2)

print("Documents préparés :", len(documents))
print("Relations sélectionnées :", len(selected_relations))
print("Fichier créé :", output_file)
print("Premier métier :", documents[0]["title"])
