
# Choix de la base vectorielle — PathForge AI

## 1. Contexte et besoins

PathForge AI est une plateforme d'orientation professionnelle
reposant sur une architecture GraphRAG hybride.

Elle exploite trois sources principales :
- Le référentiel ESCO : métiers et compétences.
- Les offres d'emploi : exigences professionnelles.
- Les CV et projets : compétences des étudiants.

Le moteur de recherche doit identifier des documents
pertinents même lorsque les compétences sont formulées
différemment.

La base vectorielle doit répondre à quatre besoins :
1. Recherche sémantique performante.
2. Recherche hybride lexicale et vectorielle.
3. Filtrage précis par métadonnées.
4. Déploiement local reproductible.

## 2. Comparaison des solutions

Trois solutions ont été étudiées :
Qdrant, Milvus et pgvector.

| Critère | Qdrant | Milvus | pgvector |
|---|---|---|---|
| Recherche dense | Native | Native | Extension PostgreSQL |
| Recherche hybride | Dense + sparse / BM25 | Dense + sparse | Vecteurs + Full-Text Search |
| Filtrage par métadonnées | Payload JSON et index | Filtres scalaires | WHERE SQL et index |
| Index HNSW | Oui | Oui | Oui |
| Déploiement local | Docker simple | Docker, plusieurs composants possibles | PostgreSQL + extension |
| Intégration Python | qdrant-client | pymilvus | psycopg / SQLAlchemy |
| Pertinence pour PathForge | Très adaptée | Adaptée | Alternative crédible |

## 3. Critère 1 — Filtrage par métadonnées

PathForge doit pouvoir restreindre les recherches
selon différents critères :

- Métier cible : Data Engineer, AI Engineer, etc.
- Type de document : CV, offre, projet.
- Source : ESCO, Kaggle ou profil étudiant.
- Compétence ou identifiant ESCO.
- Date de publication d'une offre.

Qdrant permet d'associer des métadonnées JSON
(payload) à chaque document vectorisé.

Exemple de métadonnées envisagées :

```json
{
  "doc_id": "job_001",
  "source": "linkedin_kaggle",
  "document_type": "job_offer",
  "job_title": "Data Engineer",
  "esco_uri": "identifiant_esco",
  "publication_year": 2024
}
```

Ces filtres permettront de rechercher uniquement
les informations pertinentes pour le métier ciblé.

Des index de payload seront configurés sur les
champs fréquemment utilisés dans les filtres.

Les données privées des étudiants devront être
isolées par des contrôles d'accès applicatifs.

## 4. Critère 2 — Latence et performances

La latence représente le temps nécessaire
pour retrouver les informations pertinentes.

Qdrant prend en charge des index de recherche
approximative HNSW et le filtrage par métadonnées.

La recherche hybride permettra de combiner :
- BM25 : correspondance lexicale.
- Embeddings : similarité sémantique.
- Fusion : combinaison des résultats.
- Cross-Encoder : reranking des candidats.

Le Cross-Encoder sera exécuté dans le pipeline
applicatif après la récupération des candidats.

Objectifs d'évaluation :
- Recall@10 >= 85 %.
- Recall@5 >= 80 %.
- Latence E2E P95 < 3,5 secondes.
- Temps d'insertion cible < 50 ms par lot
  de 64 chunks, conformément au backlog.

Ces seuils sont des objectifs à mesurer
et ne constituent pas des performances validées.

Un benchmark comparatif pourra mesurer :
- La latence de recherche.
- Le rappel des documents pertinents.
- L'impact des filtres sur les résultats.
- Le temps d'indexation.

Aucune supériorité de latence de Qdrant
sur Milvus ou pgvector n'est affirmée
sans mesures comparatives.

## 5. Critère 3 — Simplicité d'orchestration locale

Qdrant a été retenu notamment pour sa
simplicité de démarrage avec Docker Compose.

Le dépôt contient un fichier docker-compose.yml
permettant le lancement de la base vectorielle.

Version locale testée : Qdrant v1.15.5.

Commandes de démarrage :

```bash
docker compose up -d
docker compose ps
```

Interface locale :

http://localhost:6333/dashboard

Le démarrage de Qdrant et l'accès au dashboard
ont été vérifiés sur l'environnement Windows
de développement.

Le volume Docker configuré permet de conserver
les données entre les redémarrages.

Milvus offre également un déploiement Docker,
mais certaines configurations autonomes
nécessitent plusieurs services complémentaires.

pgvector constitue une alternative intéressante
si l'équipe souhaite centraliser les données
relationnelles et vectorielles dans PostgreSQL.

## 6. Complémentarité avec Neo4j

Qdrant et Neo4j répondent à deux besoins distincts.

### Qdrant — Recherche documentaire

- Stockage des embeddings.
- Recherche dense et sparse.
- Filtrage par métadonnées.
- Récupération des passages pertinents.

### Neo4j — Graphe de connaissances

- Relations entre étudiants et projets.
- Relations entre projets et compétences.
- Relations entre métiers et compétences.
- Exploration des chemins de preuves.

### LLM — Génération augmentée

Le LLM exploitera les résultats documentaires
et les relations pertinentes du graphe pour
produire des recommandations explicables.

Qdrant retrouve les informations,
Neo4j relie les concepts et
le LLM formule les explications.

## 7. Décision architecturale

La base vectorielle retenue pour
le prototype PathForge AI est Qdrant.

Cette décision est motivée par :
1. La recherche hybride dense et lexicale.
2. Le filtrage par métadonnées.
3. L'intégration Python / FastAPI.
4. La simplicité de déploiement local.
5. La complémentarité avec Neo4j.

Le choix sera confirmé par des expérimentations
mesurant la pertinence, la latence
et le comportement du moteur de recherche.

## 8. État d'avancement

- [x] Comparaison initiale des solutions.
- [x] Sélection de Qdrant.
- [x] Configuration Docker Compose.
- [x] Démarrage local de Qdrant v1.15.5.
- [x] Accès au tableau de bord vérifié.
- [ ] Création de la collection vectorielle.
- [ ] Ingestion des premiers embeddings.
- [ ] Tests de recherche hybride.
- [ ] Benchmark de latence et de pertinence.

## 9. Références techniques

- Qdrant — https://qdrant.tech/documentation/
- Milvus — https://milvus.io/docs/
- pgvector — https://github.com/pgvector/pgvector
