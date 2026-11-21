
# PathForge AI

### Transformez vos compétences en parcours professionnel

PathForge AI est une plateforme intelligente d'orientation
professionnelle destinée aux étudiants.

Elle exploite les CV, projets et expériences académiques
pour identifier les compétences documentées, les comparer
aux exigences d'un métier cible et proposer des
recommandations personnalisées et explicables.

## Problématique

Les étudiants acquièrent des compétences au cours de leurs
études, mais disposent rarement d'une vision claire de leur
adéquation avec les exigences du marché de l'emploi.

Les outils classiques de CV matching reposent essentiellement
sur des mots-clés, sans toujours prendre en compte les
relations entre compétences, projets et métiers.

## Notre solution

PathForge AI s'appuie sur une architecture GraphRAG hybride
combinant recherche documentaire et graphe de connaissances.

La plateforme vise à permettre de :

1. Analyser un CV et des projets académiques.
2. Identifier les compétences documentées.
3. Sélectionner un métier cible.
4. Comparer les compétences du profil aux exigences du métier.
5. Identifier les écarts et preuves manquantes.
6. Générer des recommandations justifiées par des sources.

## Technologies principales

| Domaine | Technologies |
|---|---|
| Langage principal | Python |
| Backend | FastAPI |
| Frontend | React |
| Recherche vectorielle | Qdrant |
| Graphe de connaissances | Neo4j |
| Recherche hybride | BM25 + embeddings |
| Reranking | Cross-Encoder |
| Génération | LLM |
| Base relationnelle | PostgreSQL |
| Évaluation | Ragas |
| Conteneurisation | Docker Compose |

## Sources de données

- Référentiel européen ESCO.
- Offres d'emploi historiques issues d'un corpus public.
- Profils étudiants fictifs ou anonymisés.

Le référentiel ESCO et un sous-ensemble de relations
métiers-compétences sont déjà présents dans le dépôt.

## Démarrage local

### Prérequis

- Git
- Docker Desktop
- Docker Compose

### Lancer Qdrant

Depuis la racine du dépôt :

    docker compose up -d

Vérifier le conteneur :

    docker compose ps

Tableau de bord :

http://localhost:6333/dashboard

Pour arrêter les services :

    docker compose down

Ces commandes démarrent actuellement Qdrant.
Le reste de la plateforme est en cours de développement.

## Documentation

| Document | Description |
|---|---|
| [Fiche de cadrage](docs/fiche_cadrage_ingenierie.md) | Contexte, objectifs et contraintes |
| [Architecture technique](docs/architecture.md) | Organisation et flux techniques |
| [Choix de Qdrant](docs/choix_base_vectorielle.md) | Comparaison des bases vectorielles |
| [Backlog MoSCoW](docs/backlog_moscow.md) | Fonctionnalités et priorités |
| [Répartition de l'équipe](docs/repartition_equipe.md) | Responsabilités et collaboration |

## Équipe

- Essaied Nour — 
- Fourati Yosr — 
- Trabelsi Nidhal — 

## État du projet

Le projet est actuellement au stade de cadrage technique
et de préparation des premières données.

Les datasets ESCO ont été intégrés et vérifiés,
et Qdrant a été démarré localement avec Docker.

L'architecture GraphRAG complète constitue
l'objectif de développement des prochaines étapes.

## Limites

PathForge AI est un outil d'aide à l'orientation.

Il ne certifie pas les compétences d'un étudiant
et ne garantit ni son employabilité ni son recrutement.
