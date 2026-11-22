
# Répartition de l'équipe — PathForge AI

## 1. Composition de l'équipe

Le projet PathForge AI est réalisé par trois membres.

| Membre | Rôle principal |
|---|---|
| Essaied Nour | à remplir |
| Fourati Yosr  | à remplir |
| Trabelsi Nidhal | à remplir |

L'organisation repose sur une répartition
des responsabilités principales et une collaboration
sur les interfaces entre modules.

## 2. Responsabilités principales

###  — Data / Retrieval

Responsabilités :

- Préparation et nettoyage des datasets.
- Exploitation du référentiel ESCO.
- Extraction et normalisation des compétences.
- Préparation du corpus documentaire.
- Génération des embeddings.
- Indexation dans Qdrant.
- Recherche hybride BM25 et dense.
- Expérimentation du reranking.

###  — Backend / MLOps

Responsabilités :

- Conception des endpoints FastAPI.
- Validation des entrées avec Pydantic.
- Orchestration du pipeline GraphRAG.
- Intégration de Neo4j et du LLM.
- Logique de comparaison des compétences.
- Génération des recommandations sourcées.
- Tests backend.
- Évaluation et suivi de la qualité.

###  — Frontend / Infra

Responsabilités :

- Développement de l'interface React.
- Parcours utilisateur.
- Import des profils.
- Affichage des compétences et écarts.
- Visualisation des recommandations.
- Gestion des états et erreurs frontend.
- Configuration Docker Compose.
- Préparation de l'environnement local.

## 3. Matrice de responsabilités

**Légende :**

- R : Responsable principal.
- C : Contributeur ou collaborateur.
- - : Intervention ponctuelle si nécessaire.

| Module | membre1 | membre2 | membre3 |
|---|---|---|---|
| Préparation des datasets | R | C | - |
| Normalisation ESCO | R | C | - |
| Embeddings et Qdrant | R | C | - |
| Recherche hybride | R | C | - |
| Reranking | R | C | - |
| Modèle et intégration Neo4j | C | R | - |
| FastAPI | - | R | C |
| Orchestration GraphRAG | C | R | C |
| Analyse des écarts | C | R | C |
| Intégration du LLM | C | R | - |
| Frontend React | - | C | R |
| Docker Compose | C | C | R |
| Tests et intégration | C | R | C |
| Documentation | C | R | C |

Cette matrice est une proposition de répartition
opérationnelle à valider par l'équipe.

## 4. Organisation sur GitHub

### Branches

- `main` : version intégrée.
- `feature/data-*` : ingestion et recherche.
- `feature/backend-*` : API et moteur GraphRAG.
- `feature/frontend-*` : interface utilisateur.
- `feature/infra-*` : infrastructure.

### Workflow proposé

1. Créer une issue pour chaque fonctionnalité.
2. Créer une branche dédiée.
3. Développer et tester la modification.
4. Ouvrir une Pull Request.
5. Faire relire le code.
6. Fusionner après validation.

Les modifications importantes doivent passer
par une Pull Request lorsque cela est possible.

## 5. Collaboration entre modules

### Data vers Backend

Définir ensemble :

- Format des documents indexés.
- Métadonnées nécessaires.
- Contrat des résultats de recherche.
- Identifiants ESCO et provenance.

### Backend vers Frontend

Définir ensemble :

- Routes de l'API.
- Format des requêtes.
- Format des réponses.
- Gestion des erreurs.
- Structure des citations.
- Streaming SSE.

### Infrastructure

Les services doivent être configurés
avec des variables d'environnement documentées.

Les secrets ne doivent jamais être ajoutés
au dépôt GitHub public.

## 6. Règles de qualité

- Code lisible et documenté.
- Commits explicites.
- Tests avant intégration.
- Respect de la structure du dépôt.
- Revue des modifications importantes.
- Mise à jour de la documentation pertinente.

## 7. Suivi du travail

Le suivi sera assuré au moyen :

- Des issues GitHub.
- Des Pull Requests.
- Du backlog MoSCoW.
- Des commits et revues de code.

L'objectif est de garantir
la traçabilité des contributions
et l'intégration cohérente des différents modules.
