
# Backlog MoSCoW — PathForge AI

## 1. Objectif

Le backlog organise les fonctionnalités
et exigences techniques du projet selon
la méthode MoSCoW.

Les priorités sont :

- Must Have : indispensables au prototype.
- Should Have : importantes, mais secondaires.
- Could Have : améliorations facultatives.
- Won't Have : exclues du périmètre initial.

Les identifiants US permettent de suivre
chaque fonctionnalité pendant le développement.

---

## 2. Must Have

### US-01 — Ingestion documentaire

**En tant que** système,
**je veux** ingérer les CV, projets et sources métier,
**afin de** constituer un corpus exploitable.

Critères d'acceptation :

- Lecture des formats retenus.
- Extraction des textes.
- Nettoyage des documents.
- Conservation des métadonnées.
- Traçabilité de la provenance.

### US-02 — Indexation vectorielle

**En tant que** système,
**je veux** créer des embeddings et les indexer,
**afin de** permettre la recherche sémantique.

Critères d'acceptation :

- Découpage documentaire opérationnel.
- Génération d'embeddings.
- Collection Qdrant créée.
- Points indexés avec métadonnées.
- Recherche vectorielle testée.

### US-03 — Recherche hybride et reranking

**En tant que** étudiant,
**je veux** retrouver les informations pertinentes,
**afin de** comprendre les exigences d'un métier.

Critères d'acceptation :

- Recherche lexicale.
- Recherche dense.
- Fusion des résultats.
- Reranking des candidats.
- Retour des passages et sources.

### US-04 — API FastAPI

**En tant que** client applicatif,
**je veux** accéder aux fonctionnalités par API,
**afin de** communiquer avec le moteur GraphRAG.

Critères d'acceptation :

- Routes API documentées.
- Validation Pydantic.
- Gestion des erreurs.
- Réponses structurées.
- Tests des endpoints principaux.

### US-05 — Streaming des réponses

**En tant que** étudiant,
**je veux** voir la réponse progressivement,
**afin de** ne pas attendre la génération complète.

Critères d'acceptation :

- Endpoint SSE opérationnel.
- Affichage progressif.
- Gestion des interruptions.
- Gestion des erreurs de génération.

### US-06 — Interface React

**En tant que** étudiant,
**je veux** utiliser une interface simple,
**afin de** analyser mon parcours.

Critères d'acceptation :

- Import d'un profil.
- Sélection du métier cible.
- Lancement de l'analyse.
- Affichage des résultats.
- Consultation des sources.

### US-07 — Tests et intégration continue

**En tant que** équipe,
**nous voulons** automatiser les contrôles,
**afin de** limiter les régressions.

Critères d'acceptation :

- Tests Pytest.
- Linting Ruff.
- Workflow GitHub Actions.
- Signalement des erreurs.

### US-08 — Conteneurisation

**En tant que** développeur,
**je veux** lancer les services localement,
**afin de** disposer d'un environnement reproductible.

Critères d'acceptation :

- Docker Compose configuré.
- Variables documentées.
- Volumes persistants si nécessaires.
- Démarrage des services documenté.

### US-15 — Extraction et normalisation ESCO

**En tant que** système,
**je veux** rapprocher les compétences extraites
des concepts ESCO,
**afin de** comparer des profils hétérogènes.

Critères d'acceptation :

- Extraction des compétences.
- Correspondance avec ESCO.
- Conservation des identifiants.
- Signalement des cas ambigus.
- Validation sur un échantillon annoté.

### US-16 — Graphe de connaissances Neo4j

**En tant que** système,
**je veux** structurer les relations
entre étudiants, projets, compétences et métiers,
**afin de** retrouver des chemins de preuves.

Critères d'acceptation :

- Schéma des entités défini.
- Relations documentées.
- Import des données ESCO.
- Requêtes Cypher fonctionnelles.
- Provenance des relations conservée.

### US-17 — Analyse des écarts

**En tant que** étudiant,
**je veux** comparer mon profil à un métier cible,
**afin de** connaître les compétences
que je dois encore documenter ou développer.

Critères d'acceptation :

- Identification des compétences documentées.
- Extraction des exigences du métier.
- Comparaison des compétences.
- Distinction entre absence et manque de preuve.
- Recommandations personnalisées et sourcées.

---

## 3. Should Have

### US-09 — Observabilité

Mettre en place un suivi des requêtes et
des étapes du pipeline, par exemple avec Langfuse.

Critères :

- Traces des requêtes.
- Identification des erreurs.
- Suivi des temps d'exécution.
- Pas de divulgation de données sensibles.

### US-10 — Cache

Mettre en cache certains résultats
afin de réduire les calculs redondants.

Une solution comme Redis pourra être étudiée.

Critères :

- Cache activable.
- Stratégie d'expiration.
- Mesure de son effet sur la latence.

### US-11 — Évaluation automatisée

Mettre en place une évaluation reproductible
des recherches et réponses avec Ragas
et un jeu de données annoté.

Critères :

- Jeu de test documenté.
- Mesure des métriques choisies.
- Rapport de résultats.
- Comparaison entre configurations.

---

## 4. Could Have

### US-12 — Déploiement Kubernetes

Étudier un déploiement orchestré
si le prototype évolue vers une infrastructure distribuée.

### US-13 — Agents spécialisés

Explorer des agents capables
de coordonner différentes tâches d'analyse.

### US-14 — OCR avancé

Ajouter la prise en charge des CV scannés
nécessitant une reconnaissance optique de caractères.

---

## 5. Won't Have — Version initiale

Les fonctionnalités suivantes ne sont pas prévues
pour le prototype initial :

- Certification officielle des compétences.
- Recrutement automatique.
- Décision d'embauche automatisée.
- Surveillance exhaustive du marché en temps réel.
- Déploiement industriel à grande échelle.

---

## 6. Dépendances principales

| Fonctionnalité | Dépend de |
|---|---|
| US-02 Indexation | US-01 Ingestion |
| US-03 Recherche hybride | US-02 Indexation |
| US-16 Neo4j | US-15 Normalisation ESCO |
| US-17 Analyse des écarts | US-03 et US-16 |
| US-04 API | Interfaces des modules métier |
| US-05 Streaming | US-04 API |
| US-06 Frontend | US-04 API |
| US-11 Évaluation | Pipeline de recherche fonctionnel |

La réalisation des fonctionnalités sera progressive.

Le statut exact de chaque US devra être suivi
dans les issues ou le tableau de projet GitHub.

## 7. Définition de terminé

Une User Story est considérée comme terminée lorsque :

- La fonctionnalité est développée.
- Les critères d'acceptation sont validés.
- Les tests nécessaires sont passés.
- Le code est revu.
- La documentation est mise à jour.
- Le changement est intégré au dépôt.
