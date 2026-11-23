
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT / "data" / "processed"
    / "esco_documents_clean.json"
)

QUESTIONS_FILE = (
    ROOT / "data" / "benchmark"
    / "questions.json"
)

with DATA_FILE.open("r", encoding="utf-8") as f:
    documents = json.load(f)

with QUESTIONS_FILE.open("r", encoding="utf-8") as f:
    questions = json.load(f)

# Index des métiers par titre
occupations = {}

for doc in documents:
    title = doc["title"].strip().casefold()
    occupations.setdefault(title, []).append(doc)

print("\n===== VÉRIFICATION BENCHMARK =====")

valid = 0
missing = []

for question in questions:
    expected = question["expected_occupation"]
    matches = occupations.get(expected.strip().casefold(), [])

    print(f"\n{question['id']} : {expected}")

    if len(matches) == 1:
        doc = matches[0]
        question["expected_uri"] = doc["id"]

        print("Statut : OK")
        print("URI :", doc["id"])
        valid += 1

    elif len(matches) > 1:
        print("Statut : AMBIGU")
        missing.append(expected)

    else:
        print("Statut : INTROUVABLE")
        missing.append(expected)

print("\n===== BILAN =====")
print("Questions :", len(questions))
print("Métiers validés :", valid)
print("Métiers à vérifier :", len(missing))

if missing:
    print("\nMétiers non validés :")
    for name in missing:
        print("-", name)
else:
    with QUESTIONS_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            questions,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\nToutes les références sont validées.")
    print("URI ESCO ajoutées à questions.json.")
