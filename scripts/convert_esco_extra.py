
import csv
import json
from pathlib import Path

SOURCE = Path("data/temp/esco_csv")
DESTINATION = Path("data/raw/esco")

FILES = {
    "skillSkillRelations_en.csv": "skill_skill_relations.json",
    "broaderRelationsOccPillar_en.csv": "occupation_hierarchy.json",
    "broaderRelationsSkillPillar_en.csv": "skill_hierarchy.json",
    "ISCOGroups_en.csv": "isco_groups.json",
    "digitalSkillsCollection_en.csv": "digital_skills.json",
}

DESTINATION.mkdir(parents=True, exist_ok=True)

for csv_name, json_name in FILES.items():
    source = SOURCE / csv_name
    output = DESTINATION / json_name

    if not source.exists():
        raise FileNotFoundError(f"Fichier introuvable : {source}")

    if output.exists():
        raise FileExistsError(
            f"Le fichier existe déjà : {output}. "
            "Conversion arrêtée pour éviter de l'écraser."
        )

    with source.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"Fichier vide : {source}")

    with output.open("w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)

    with output.open("r", encoding="utf-8") as file:
        verified = json.load(file)

    assert len(verified) == len(rows)

    print(f"[OK] {json_name} : {len(verified)} enregistrements")

print("\nConversion des 5 fichiers terminée.")
