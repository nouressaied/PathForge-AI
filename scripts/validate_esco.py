
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data" / "raw" / "esco"

def load_csv(filename):
    with open(BASE / filename, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

occupations = load_csv("occupations_en.csv")
skills = load_csv("skills_en.csv")
relations = load_csv("occupationSkillRelations_data_ai_en.csv")

print("Métiers :", len(occupations))
print("Compétences :", len(skills))
print("Relations filtrées :", len(relations))

occupation_ids = {row["conceptUri"] for row in occupations}
skill_ids = {row["conceptUri"] for row in skills}

invalid_occupations = [
    row for row in relations
    if row["occupationUri"] not in occupation_ids
]

invalid_skills = [
    row for row in relations
    if row["skillUri"] not in skill_ids
]

print("Relations avec métier inconnu :", len(invalid_occupations))
print("Relations avec compétence inconnue :", len(invalid_skills))

if not invalid_occupations and not invalid_skills:
    print("VALIDATION REUSSIE : toutes les relations sont cohérentes.")
else:
    print("VALIDATION ECHOUEE : certaines relations sont invalides.")
    raise SystemExit(1)
