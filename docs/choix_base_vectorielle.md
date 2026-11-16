
# Choix de la base vectorielle — PathForge AI

## 1. Contexte

PathForge AI repose sur une architecture GraphRAG hybride
qui analyse les compétences des étudiants et les compare
aux exigences des métiers.

Le moteur de recherche doit retrouver les informations
pertinentes dans les CV, les projets, les offres d'emploi
et le référentiel ESCO.

## 2. Bases vectorielles étudiées

Nous avons considéré trois solutions :
Qdrant, Milvus et pgvector.

| Critère | Qdrant | Milvus | pgvector |
|---|---|---|---|
| Recherche vectorielle | Oui | Oui | Oui |
| Recherche hybride | Dense + sparse | Dense + sparse | SQL + FTS |
| Filtrage par métadonnées | Oui | Oui | Oui, via SQL |
| Déploiement local | Simple | Plus complexe | Simple avec PostgreSQL |
| Intégration Python | Oui | Oui | Oui |
| Adaptation au prototype | Très bonne | Bonne | Très bonne |

## 3. Justification du choix

Nous retenons Qdrant pour les raisons suivantes :

- Recherche sémantique par embeddings.
- Prise en charge de la recherche hybride dense/sparse.
- Filtrage des résultats par métadonnées.
- Intégration avec Python et FastAPI.
- Déploiement local simple avec Docker.
- Adaptation à un prototype GraphRAG.

## 4. Complémentarité avec Neo4j

Qdrant servira à retrouver les documents pertinents.

Neo4j représentera les relations entre les étudiants,
les projets, les compétences, les offres et les métiers.

Le LLM exploitera ces informations pour générer
des recommandations personnalisées et sourcées.

## 5. Décision

Qdrant est retenu comme base vectorielle initiale
pour PathForge AI.

Ce choix sera évalué expérimentalement à travers
la pertinence des résultats et les mesures de latence.
