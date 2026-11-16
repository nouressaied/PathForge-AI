
# ESCO Dataset — PathForge AI

## 1. Description

ESCO (European Skills, Competences, Qualifications and Occupations)
est un référentiel officiel européen qui décrit les métiers,
les compétences et leurs relations.

Version : ESCO v1.2.1
Langue : English
Format : CSV

## 2. Source officielle

https://esco.ec.europa.eu/en/use-esco/download

## 3. Fichiers disponibles

| Fichier | Description | Statut |
|---|---|---|
| occupations_en.csv | Référentiel des métiers | Intégré |
| skills_en.csv | Référentiel des compétences | Intégré |
| occupationSkillRelations_data_ai_en.csv | Relations filtrées pour les métiers Data/IA | Intégré |

## 4. Filtrage des relations

Le fichier original occupationSkillRelations_en.csv
contient les relations entre les métiers et les compétences.

Pour le premier prototype de PathForge AI,
un sous-ensemble thématique a été constitué :

- 8 métiers orientés Data, IA et développement logiciel.
- 674 relations métiers-compétences.
- Identifiants ESCO conservés pour maintenir
  les correspondances avec les autres fichiers.

Ce fichier est un sous-ensemble de travail
et non l'intégralité du référentiel ESCO.

## 5. Utilisation dans PathForge AI

Les données permettront de :

1. Identifier les compétences associées aux métiers.
2. Normaliser les compétences extraites des CV et projets.
3. Construire un graphe de connaissances dans Neo4j.
4. Comparer les compétences documentées des étudiants
   aux exigences du métier cible.
5. Justifier les recommandations grâce aux relations ESCO.

## 6. Technologies associées

- Python / Pandas : préparation et validation des CSV.
- Neo4j : relations métiers-compétences.
- Qdrant : recherche hybride sur les contenus indexés.
- GraphRAG : génération de recommandations sourcées.

## 7. État d'avancement

- [x] Téléchargement d'ESCO v1.2.1.
- [x] Ajout de occupations_en.csv.
- [x] Ajout de skills_en.csv.
- [x] Préparation du fichier filtré des relations.
- [x] Ajout du fichier filtré sur GitHub.
- [ ] Vérification des relations et des identifiants ESCO.
- [ ] Prétraitement et indexation des données.
- [ ] Construction du graphe Neo4j.
