
# PathForge AI

## Présentation
PathForge AI est une plateforme intelligente d'orientation
professionnelle basée sur une architecture GraphRAG hybride.

Elle analyse les CV, projets et expériences des étudiants,
puis les compare aux compétences exigées par les métiers
afin de proposer des recommandations personnalisées et sourcées.

## Problématique
Comment relier les compétences des étudiants aux exigences
réelles du marché de l'emploi pour identifier les écarts
et construire un parcours professionnel adapté ?

## Objectifs
- Extraire les compétences des CV et projets étudiants.
- Analyser les offres d'emploi et le référentiel ESCO.
- Identifier les compétences documentées et manquantes.
- Construire un graphe de connaissances.
- Générer des recommandations personnalisées et explicables.

## Données
- ESCO : référentiel européen des métiers et compétences.
- Adzuna API : offres d'emploi réelles.
- CV et projets étudiants : exemples fictifs ou données autorisées.

## Architecture
Sources de données → Ingestion et normalisation
→ Recherche hybride (BM25 + embeddings)
→ Qdrant + Reranking
→ Graphe Neo4j
→ LLM → Recommandations sourcées

## Technologies
- Python, FastAPI, React
- Qdrant, Neo4j, PostgreSQL
- BM25, Embeddings, Cross-Encoder
- LangChain ou LlamaIndex
- Ragas, Langfuse
- Docker, GitHub Actions

## Objectifs d'évaluation
- Recall@10 ≥ 85 %
- Faithfulness ≥ 0,85
- Latence P95 < 3,5 secondes

Ces valeurs sont des objectifs à valider expérimentalement.

## Équipe
- Membre 1 : collecte et préparation des datasets
- Membre 2 : architecture GraphRAG
- Membre 3 : backend, Docker, tests et intégration

La répartition définitive sera précisée par l'équipe.

## État du projet
Phase actuelle : cadrage et préparation des livrables S2.
