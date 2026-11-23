
from pathlib import Path
import pandas as pd

# Chemin du dataset ESCO
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "esco"

files = {
    "Métiers": "occupations_en.csv",
    "Compétences": "skills_en.csv",
    "Relations": "occupationSkillRelations_en.csv",
}

for name, filename in files.items():
    print(f"\n===== {name} =====")

    df = pd.read_csv(DATA_DIR / filename, low_memory=False)

    print("Nombre de lignes :", len(df))
    print("Colonnes :", df.columns.tolist())
    print("\nExemple :")
    print(df.head(2).to_string(index=False))
