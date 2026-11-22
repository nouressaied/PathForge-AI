
# PathForge AI

### Transformez vos compétences en parcours professionnel

PathForge AI est une plateforme intelligente d'orientation
professionnelle destinée aux étudiants.

Elle analyse les compétences documentées par les CV,
les projets et les expériences académiques, puis les compare
aux exigences d'un métier cible afin de proposer des
recommandations personnalisées, explicables et sourcées.

## 1. Problématique

Les étudiants développent de nombreuses compétences
au cours de leurs formations, stages et projets.

Cependant, ils disposent rarement d'une vision claire
de l'adéquation entre leurs compétences et les exigences
des métiers qu'ils souhaitent exercer.

Les approches classiques de rapprochement entre profils
et métiers ne prennent pas toujours en compte les preuves
issues des projets ni les relations entre les compétences.

**Comment relier les compétences documentées d'un étudiant
aux exigences professionnelles d'un métier, tout en
justifiant les recommandations proposées ?**

## 2. Notre solution

PathForge AI repose sur une architecture GraphRAG hybride,
combinant recherche documentaire, graphe de connaissances
et génération augmentée par un LLM.

La plateforme vise à permettre de :

1. Analyser un CV, des projets et des expériences académiques.
2. Identifier les compétences déclarées et documentées.
3. Sélectionner un métier cible.
4. Retrouver les compétences exigées pour ce métier.
5. Identifier les écarts et les preuves insuffisantes.
6. Proposer des recommandations personnalisées et sourcées.

L'objectif est d'accompagner l'étudiant dans
sa progression professionnelle, sans prétendre
certifier automatiquement ses compétences.

## 3. Architecture générale

PathForge AI s'appuie sur deux pipelines complémentaires.

### Pipeline 1 — Ingestion et indexation

**Sources : ESCO, offres d'emploi, CV et projets**

↓

**Extraction et préparation des données**

↓

**Normalisation des compétences et chunking**

↓

**Génération des embeddings**

↓

**Indexation Qdrant et construction du graphe Neo4j**

### Pipeline 2 — Recherche et génération

**React — Interface étudiant**

↓

**FastAPI — Orchestration**

↓

**Recherche hybride Qdrant + Exploration Neo4j**

↓

**Fusion des résultats et reranking**

↓

**Construction du contexte GraphRAG**

↓

**LLM — Analyse des écarts et recommandations sourcées**

PostgreSQL est prévu pour le stockage des données
applicatives autorisées.

Cette architecture représente la cible technique
du projet. Tous les composants ne sont pas
encore implémentés.

Pour plus de détails :
[Architecture technique](docs/architecture.md).

## 4. Technologies principales

| Domaine | Technologie |
|---|---|
| Langage principal | Python |
| Backend | FastAPI |
| Frontend | React |
| Base vectorielle | Qdrant |
| Graphe de connaissances | Neo4j |
| Recherche hybride | BM25 + embeddings |
| Reranking | Cross-Encoder |
| Génération augmentée | LLM |
| Base relationnelle | PostgreSQL |
| Évaluation | Ragas |
| Conteneurisation | Docker Compose |

Ces technologies constituent l'architecture
cible du prototype.

## 5. Sources de données

PathForge AI repose sur plusieurs sources
de données complémentaires.

### ESCO — Référentiel métiers-compétences

ESCO v1.2.1 fournit les métiers, les compétences
et leurs relations.

Le référentiel complet a été converti en JSON
et validé localement :

- 3 043 métiers.
- 13 960 compétences.
- 126 051 relations métiers-compétences.

Les identifiants officiels sont conservés
afin d'assurer la cohérence entre les données.

La documentation détaillée du dataset est disponible ici :

[Dataset ESCO](data/raw/esco/README.md).

### Offres d'emploi

Un corpus d'offres d'emploi historiques
sera exploité afin d'analyser les compétences
et qualifications demandées par les employeurs.

### Profils étudiants

Des profils fictifs ou anonymisés et autorisés
seront utilisés pour expérimenter l'analyse
des compétences et les recommandations.

## 6. Démarrage local

### Prérequis

- Git
- Docker Desktop
- Docker Compose
- Python

### Démarrer les services disponibles

Depuis la racine du dépôt :

    docker compose up -d

Vérifier les conteneurs :

    docker compose ps

### Accéder à Qdrant

Tableau de bord :

http://localhost:6333/dashboard

### Arrêter les services

    docker compose down

Qdrant v1.15.5 a été démarré et vérifié localement.

Le moteur GraphRAG complet reste en cours
de développement.

## 7. Documentation

| Document | Contenu |
|---|---|
| [Fiche de cadrage](docs/fiche_cadrage_ingenierie.md) | Problématique, objectifs et contraintes |
| [Architecture technique](docs/architecture.md) | Pipelines et composants techniques |
| [Choix de Qdrant](docs/choix_base_vectorielle.md) | Comparaison Qdrant, Milvus et pgvector |
| [Backlog MoSCoW](docs/backlog_moscow.md) | Fonctionnalités et priorités |
| [Dataset ESCO](data/raw/esco/README.md) | Source, structure et validation des données |

## 8. État d'avancement

### Réalisé

- [x] Création et structuration du dépôt GitHub.
- [x] Définition de la vision produit.
- [x] Conception de l'architecture initiale.
- [x] Comparaison et sélection de Qdrant.
- [x] Configuration initiale de Docker Compose.
- [x] Démarrage local de Qdrant.
- [x] Préparation du référentiel ESCO complet en JSON.
- [x] Validation locale des 126 051 relations ESCO.

### En cours et à réaliser

- [ ] Publication du nouveau corpus JSON sur GitHub.
- [ ] Préparation du corpus pour l'ingestion.
- [ ] Implémentation du chunking.
- [ ] Génération et indexation des embeddings.
- [ ] Recherche sémantique Top-5 dans Qdrant.
- [ ] Intégration de Neo4j.
- [ ] Développement de FastAPI et React.
- [ ] Génération de recommandations avec le LLM.
- [ ] Évaluation du système.

## 9. Limites

PathForge AI est un outil d'aide à l'orientation
professionnelle.

Il ne constitue pas un outil de certification
des compétences et ne garantit ni l'employabilité
ni le recrutement d'un étudiant.

Les recommandations dépendront de la qualité
des informations fournies et des sources utilisées.
