
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ESCO_DIR = ROOT / "data" / "raw" / "esco"

FILES = {
    "occupations_en.csv": "occupations.json",
    "skills_en.csv": "skills.json",
    "occupationSkillRelations_en.csv": "occupation_skill_relations.json",
}


def convert_csv_to_json(source, destination):
    count = 0

    with source.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        with destination.open("w", encoding="utf-8") as json_file:
            json_file.write("[\n")

            for row in reader:
                if count > 0:
                    json_file.write(",\n")

                json.dump(row, json_file, ensure_ascii=False)
                count += 1

            json_file.write("\n]\n")

    return count


def main():
    print("=== CONVERSION ESCO CSV VERS JSON ===")

    for input_name, output_name in FILES.items():
        source = ESCO_DIR / input_name
        destination = ESCO_DIR / output_name

        if not source.exists():
            raise FileNotFoundError(
                f"Fichier source introuvable : {source}"
            )

        count = convert_csv_to_json(source, destination)

        print(f"{input_name} -> {output_name}")
        print(f"Documents convertis : {count}")
        print()

    print("Conversion terminee.")


if __name__ == "__main__":
    main()
