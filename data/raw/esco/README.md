
# ESCO Dataset — PathForge AI

## 1. Description

ESCO (European Skills, Competences, Qualifications and Occupations)
est un référentiel officiel de l'Union européenne qui décrit
les métiers, les compétences et les relations entre eux.

Version utilisée : ESCO v1.2.1
Langue : Anglais (en)
Format : CSV

## 2. Source officielle

https://esco.ec.europa.eu/en/use-esco/download

## 3. Fichiers du dataset

| Fichier | Description | État |
|---|---|---|
| occupations_en.csv | Liste des métiers | Intégré |
| skills_en.csv | Liste des compétences | Intégré |
| occupationSkillRelations_en.csv | Relations métiers-compétences | À intégrer |

## 4. Utilisation dans PathForge AI

Les données ESCO permettront de :

1. Identifier les compétences associées aux métiers.
2. Normaliser les compétences extraites des CV et projets.
3. Construire le graphe de connaissances avec Neo4j.
4. Comparer les compétences documentées des étudiants
   aux exigences des métiers ciblés.

## 5. Technologies associées

- Python / Pandas : préparation et nettoyage.
- Neo4j : graphe métiers-compétences.
- Qdrant : indexation et recherche hybride.
- GraphRAG : recommandations explicables et sourcées.

## 6. État d'avancement

- [x] Téléchargement du dataset ESCO v1.2.1.
- [x] Extraction de l'archive ZIP.
- [x] Ajout de occupations_en.csv sur GitHub.
- [x] Ajout de skills_en.csv sur GitHub.
- [ ] Ajout de occupationSkillRelations_en.csv.
- [ ] Validation du schéma et des relations entre fichiers.
- [ ] Prétraitement et ingestion dans Neo4j / Qdrant.

## 7. Prochaine étape

Intégrer le fichier des relations métiers-compétences,
puis préparer un sous-ensemble représentatif
des métiers Data et Intelligence Artificielle.
