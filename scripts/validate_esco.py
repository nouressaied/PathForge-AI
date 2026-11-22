
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw" / "esco"


def load_json(filename):
    path = DATA_DIR / filename

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    occupations = load_json("occupations.json")
    skills = load_json("skills.json")
    relations = load_json("occupation_skill_relations.json")

    occupation_uris = {
        row["conceptUri"]
        for row in occupations
    }

    skill_uris = {
        row["conceptUri"]
        for row in skills
    }

    unknown_occupations = []
    unknown_skills = []

    for relation in relations:
        occupation_uri = relation.get("occupationUri")
        skill_uri = relation.get("skillUri")

        if occupation_uri not in occupation_uris:
            unknown_occupations.append(occupation_uri)

        if skill_uri not in skill_uris:
            unknown_skills.append(skill_uri)

    print("=== VALIDATION ESCO JSON ===")
    print(f"Metiers : {len(occupations)}")
    print(f"Competences : {len(skills)}")
    print(f"Relations : {len(relations)}")
    print(f"Metiers inconnus : {len(unknown_occupations)}")
    print(f"Competences inconnues : {len(unknown_skills)}")

    if not unknown_occupations and not unknown_skills:
        print("VALIDATION REUSSIE : toutes les relations sont coherentes.")
    else:
        print("VALIDATION ECHOUEE : relations invalides detectees.")
        print("Exemples de metiers inconnus :", unknown_occupations[:5])
        print("Exemples de competences inconnues :", unknown_skills[:5])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
