
# Architecture technique — PathForge AI

## 1. Vue d'ensemble

PathForge AI repose sur une architecture GraphRAG hybride.

Elle combine la recherche documentaire,
l'exploration de relations métiers-compétences
et la génération augmentée par un LLM.

### Schéma logique

**Sources de données**

CV et projets | Offres d'emploi | ESCO

↓

**Ingestion**

Extraction → Nettoyage → Normalisation → Chunking

↓

**Indexation**

| Qdrant | Neo4j |
|---|---|
| Documents et vecteurs | Métiers, compétences et relations |
| Recherche dense et sparse | Chemins de preuves |

↓

**Moteur GraphRAG — FastAPI**

Recherche hybride + Exploration du graphe

↓

Fusion → Reranking → Construction du contexte

↓

**LLM — Analyse des écarts et recommandations sourcées**

↓

**React — Interface étudiant**

PostgreSQL assure le stockage applicatif
des profils et des historiques autorisés.

## 2. Pipeline d'ingestion

### Extraction

Les documents textuels sont extraits
depuis les CSV, PDF et JSON.

### Préparation

Les données sont nettoyées et normalisées.

Les compétences identifiées sont rapprochées
des concepts du référentiel ESCO.

Les correspondances incertaines sont conservées
comme telles pour éviter les associations injustifiées.

### Chunking

Les textes documentaires sont découpés
en passages exploitables.

Configuration envisagée :
- Taille : 512 tokens.
- Overlap : 64 tokens.
- Conservation des identifiants et sources.

Les relations ESCO structurées ne sont pas
découpées en chunks textuels.

### Embeddings

Modèle envisagé : `BAAI/bge-m3`.

Dimension des vecteurs denses : 1 024.

Les passages vectorisés sont indexés dans Qdrant.

Les relations structurées sont préparées pour Neo4j.

## 3. Recherche hybride

### Recherche lexicale

BM25 retrouve les passages contenant
les termes importants de la requête.

### Recherche dense

Les embeddings permettent de retrouver
des passages sémantiquement proches.

### Fusion

Les résultats des deux recherches sont
combinés, par exemple avec RRF.

### Reranking

Un Cross-Encoder tel que
`BAAI/bge-reranker-v2-m3`
réordonne les passages candidats.

Configuration envisagée :

- Top-20 pour la récupération initiale.
- Top-5 après reranking.

Qdrant assure la récupération initiale
et l'application gère le reranking.

## 4. Graphe de connaissances

### Entités

| Entité | Rôle |
|---|---|
| Etudiant | Profil analysé |
| Projet | Projet académique ou personnel |
| Competence | Compétence normalisée |
| Metier | Métier cible ou référencé |
| OffreEmploi | Offre professionnelle |

### Relations

| Source | Relation | Destination |
|---|---|---|
| Etudiant | REALISE | Projet |
| Projet | DOCUMENTE | Competence |
| Metier | REQUIERT | Competence |
| OffreEmploi | MENTIONNE | Competence |
| Etudiant | CIBLE | Metier |

### Exemple

Un projet NLP documente l'utilisation de Python.

Un métier peut exiger Python.

Neo4j permet de retrouver le lien entre
l'expérience documentée et l'exigence du métier.

Cette relation ne garantit pas à elle seule
la maîtrise complète de la compétence.

## 5. Pipeline GraphRAG

### Requête utilisateur

L'étudiant sélectionne un métier cible
et demande une analyse de son profil.

### Récupération

FastAPI orchestre :

1. La recherche hybride dans Qdrant.
2. Le reranking des passages.
3. L'exploration des relations Neo4j.
4. La récupération des preuves et sources.

### Analyse des écarts

Le système distingue :

- Compétences déclarées.
- Compétences documentées.
- Compétences exigées.
- Compétences insuffisamment documentées.

### Génération

Le LLM reçoit un contexte composé
des passages documentaires et des relations du graphe.

Il génère :

- Une synthèse du profil.
- Les exigences du métier.
- Les écarts constatés.
- Des recommandations personnalisées.
- Les références justificatives.

Les conclusions non étayées doivent être signalées.

## 6. Architecture applicative et déploiement

### FastAPI

- Validation avec Pydantic v2.
- API de gestion des profils.
- Orchestration GraphRAG.
- Interrogation Qdrant et Neo4j.
- Génération de réponses sourcées.
- Streaming SSE envisagé.

### React

- Import du CV.
- Sélection du métier cible.
- Consultation des compétences.
- Visualisation des écarts.
- Recommandations et sources.

### PostgreSQL

- Profils et paramètres.
- Historique des analyses.
- Références des documents.

### Docker Compose

Le déploiement sera réalisé progressivement.

Qdrant v1.15.5 est déjà démarré localement
avec un volume persistant.

Neo4j, PostgreSQL, FastAPI et React
seront intégrés au cours du développement.

### Principes de sécurité

- Protection des données personnelles.
- Secrets stockés hors du code source.
- Contrôle d'accès.
- Traçabilité des sources.
- Documents récupérés traités comme données non fiables.

L'architecture décrite représente la cible technique.
Elle ne signifie pas que tous les modules
sont déjà opérationnels.
