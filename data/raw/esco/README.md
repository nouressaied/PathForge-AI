
# ESCO Dataset — PathForge AI

## Description

ESCO (European Skills, Competences, Qualifications and Occupations)
est un référentiel officiel de l'Union européenne qui décrit
les métiers, les compétences et les relations entre eux.

## Source officielle

https://esco.ec.europa.eu/en/use-esco/download

## Fichiers à intégrer

- occupations_en.csv : liste des métiers.
- skills_en.csv : liste des compétences.
- occupationSkillRelations_en.csv : relations entre métiers et compétences.

Les noms exacts des fichiers seront adaptés au package téléchargé.

## Utilisation dans PathForge AI

Ce dataset permettra de :

1. Identifier les compétences associées aux métiers.
2. Normaliser les compétences extraites des CV.
3. Construire le graphe de connaissances dans Neo4j.
4. Comparer les compétences documentées des étudiants
   aux exigences des métiers.

## Technologies associées

- Python / Pandas : préparation des données.
- Neo4j : graphe métiers-compétences.
- Qdrant : indexation et recherche sémantique.
- GraphRAG : recommandations explicables.

## État du dataset

Source identifiée. Fichiers CSV à télécharger et à intégrer.
