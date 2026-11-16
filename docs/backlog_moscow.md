
# Backlog Technique MoSCoW — PathForge AI

## Projet Fédérateur AI-BD_BI
### Découpage Agile des User Stories & Critères d'Acceptation

**Projet :** PathForge AI — Plateforme intelligente d'analyse des
compétences et d'orientation professionnelle par GraphRAG hybride.

**Équipe :**
- Fourati Yosr — Lead Data / Retrieval
- Essaied Nour — Lead Backend / MLOps
- Trabelsi Nidhal — Lead Frontend / Infra

**Dépôt GitHub :**
https://github.com/nouressaied/PathForge-AI

---

## 1. Présentation du Backlog

Ce backlog définit les fonctionnalités et les exigences techniques
de PathForge AI selon la méthode de priorisation MoSCoW.

La plateforme vise à analyser les compétences documentées par
les CV, les projets et les stages des étudiants, puis à les
comparer aux exigences des métiers à partir du référentiel ESCO
et d'offres d'emploi.

Le système repose sur une architecture GraphRAG hybride
combinant Qdrant, Neo4j et un LLM.

Les fonctionnalités sont classées selon quatre niveaux :

- **Must Have :** indispensables à la livraison finale.
- **Should Have :** importantes, mais non bloquantes.
- **Could Have :** fonctionnalités avancées optionnelles.
- **Won't Have :** exclues du périmètre de cette version.

---

## 2. MUST HAVE — Indispensables pour la livraison finale S7

### US-01 — Ingestion et Chunking Structuré

**User Story :**

En tant que Data Engineer, je veux ingérer les CV, les
descriptions de projets, les offres d'emploi et les données
ESCO afin de préparer leur indexation et leur exploitation.

**Critères d'acceptation (DoD) :**

- Script Python asynchrone avec gestion des erreurs.
- Lecture des fichiers PDF, CSV et JSON.
- Nettoyage des données et traitement des doublons.
- Découpage des documents textuels en chunks.
- Conservation des métadonnées :
  `doc_id`, `chunk_id`, `source`, `job_id`, `profile_id`.
- Préservation des relations structurées ESCO.
- Journalisation des erreurs d'ingestion.

**Séance cible :** S2

**Responsable :** Fourati Yosr

---

### US-02 — Indexation Vectorielle HNSW

**User Story :**

En tant que moteur RAG, je veux indexer les représentations
vectorielles des documents afin de retrouver rapidement
les informations pertinentes.

**Critères d'acceptation (DoD) :**

- Qdrant démarré localement via Docker Compose.
- Création d'une collection vectorielle.
- Configuration de l'index HNSW avec distance Cosine.
- Génération des embeddings avec BAAI/bge-m3.
- Dimension des vecteurs denses : 1024.
- Conservation des métadonnées associées aux vecteurs.
- Insertion par lots de 64 chunks.
- Objectif de temps d'insertion inférieur à 50 ms
  par lot, à mesurer expérimentalement.
- Vérification de la persistance des données.

**Séance cible :** S2

**Responsable :** Fourati Yosr

---

### US-03 — Recherche Hybride et Reranking

**User Story :**

En tant qu'étudiant, je veux retrouver les offres et les
compétences pertinentes, même lorsque les formulations
diffèrent de celles utilisées dans mon CV.

**Critères d'acceptation (DoD) :**

- Recherche lexicale BM25.
- Recherche sémantique par embeddings.
- Fusion des résultats denses et sparse.
- Récupération initiale des 20 résultats pertinents.
- Reranking avec un Cross-Encoder.
- Sélection finale des 5 meilleurs résultats.
- Conservation des identifiants et sources.
- Mesure du Recall@5 sur un jeu de requêtes annotées.
- Objectif Recall@5 >= 80 %.

**Séance cible :** S3

**Responsable :** Fourati Yosr

---

### US-04 — API REST FastAPI et Schémas Pydantic v2

**User Story :**

En tant qu'application cliente, je veux interroger le moteur
PathForge AI à travers une API REST structurée afin
d'obtenir des résultats fiables et exploitables.

**Critères d'acceptation (DoD) :**

- Backend développé avec FastAPI.
- Schémas de validation Pydantic v2.
- Endpoint d'import et d'analyse du profil.
- Endpoint de recherche des métiers.
- Endpoint d'analyse des écarts de compétences.
- Endpoint de génération des recommandations.
- Validation stricte des entrées.
- Réponse HTTP 422 pour les données invalides.
- Documentation Swagger / OpenAPI disponible.
- Gestion structurée des erreurs.

**Séance cible :** S4

**Responsable :** Essaied Nour

---

### US-05 — Génération de Réponses en Streaming SSE

**User Story :**

En tant qu'étudiant, je veux recevoir progressivement les
explications de PathForge AI afin de consulter les
recommandations sans attendre la génération complète.

**Critères d'acceptation (DoD) :**

- Endpoint `/api/v1/chat/stream`.
- Streaming via Server-Sent Events (SSE).
- Transmission progressive des réponses générées.
- Association des recommandations aux sources utilisées.
- Gestion des interruptions de connexion.
- Gestion des erreurs de génération.
- Mesure du Time-to-First-Token.
- Objectif TTFT < 800 ms, à valider expérimentalement.

**Séance cible :** S4–S5

**Responsable :** Essaied Nour

---

### US-06 — Interface Web Réactive

**User Story :**

En tant qu'étudiant, je veux importer mon CV, sélectionner
un métier cible et consulter les résultats de l'analyse
afin de comprendre mon parcours professionnel.

**Critères d'acceptation (DoD) :**

- Interface développée avec React.
- Import des CV et des informations du profil.
- Sélection du métier cible.
- Affichage des compétences documentées.
- Affichage des compétences exigées.
- Visualisation des écarts de compétences.
- Consultation des recommandations personnalisées.
- Affichage des sources et justifications.
- Gestion des états loading, success et error.
- Navigation sans rechargement complet de la page.

**Séance cible :** S5

**Responsable :** Trabelsi Nidhal

---

### US-07 — Assurance Qualité et CI/CD Automatisée

**User Story :**

En tant que développeur, je veux automatiser les tests et
les contrôles de qualité afin de prévenir les régressions
et de garantir la stabilité du projet.

**Critères d'acceptation (DoD) :**

- Au moins 4 tests automatisés avec Pytest.
- Mock du LLM et de la base vectorielle.
- Vérification de la validation des requêtes API.
- Test du fonctionnement de la recherche.
- Test de la génération des recommandations.
- Analyse statique avec Ruff.
- Workflow CI/CD avec GitHub Actions.
- Échec du pipeline si les tests échouent.
- Contrôles de fusion sur la branche main.

**Séance cible :** S6

**Responsable :** Essaied Nour

---

### US-08 — Conteneurisation de Production

**User Story :**

En tant qu'ingénieur DevOps, je veux conteneuriser les
différents composants de PathForge AI afin de garantir
un déploiement reproductible.

**Critères d'acceptation (DoD) :**

- Dockerfile multi-stage pour les applications.
- Exécution des services avec utilisateur non-root.
- Docker Compose multi-services.
- Intégration de FastAPI, React, Qdrant et Neo4j.
- Intégration de PostgreSQL si nécessaire.
- Réseaux Docker internes.
- Variables d'environnement pour les secrets.
- Vérification du démarrage des services.
- Documentation des commandes de déploiement.

**Séance cible :** S7

**Responsable :** Trabelsi Nidhal

---

### US-15 — Extraction et Normalisation des Compétences ESCO

**User Story :**

En tant qu'étudiant, je veux que PathForge identifie
les compétences présentes dans mes projets et expériences
afin de construire un profil de compétences exploitable.

**Critères d'acceptation (DoD) :**

- Extraction des compétences depuis les CV et projets.
- Identification des technologies et connaissances.
- Normalisation à partir du référentiel ESCO.
- Conservation des identifiants ESCO.
- Gestion des synonymes et formulations équivalentes.
- Identification des correspondances ambiguës.
- Distinction entre compétences déclarées et documentées.
- Validation sur un jeu de profils annotés.
- Mesure de la précision et du rappel de l'extraction.

**Séance cible :** S2–S3

**Responsable :** Fourati Yosr

---

### US-16 — Construction du Graphe de Connaissances Neo4j

**User Story :**

En tant que moteur GraphRAG, je veux construire un graphe
reliant les étudiants, les projets, les compétences et
les métiers afin d'expliquer les correspondances.

**Critères d'acceptation (DoD) :**

- Création des nœuds :
  Etudiant, Projet, Competence, Metier et OffreEmploi.
- Création des relations :
  REALISE, DOCUMENTE, REQUIERT, MENTIONNE et CIBLE.
- Importation des relations métiers-compétences ESCO.
- Conservation des identifiants ESCO.
- Absence de relations orphelines.
- Requêtes Cypher permettant de retrouver les compétences
  documentées par un étudiant.
- Requêtes Cypher permettant de retrouver les compétences
  exigées pour un métier.
- Construction de chemins de preuves vérifiables.

**Séance cible :** S3–S4

**Responsables :** Fourati Yosr / Essaied Nour

---

### US-17 — Analyse des Écarts et Recommandations Explicables

**User Story :**

En tant qu'étudiant, je veux comparer mes compétences
documentées aux compétences exigées par un métier cible
afin d'identifier celles que je dois développer.

**Critères d'acceptation (DoD) :**

- Sélection d'un métier cible.
- Récupération des exigences associées au métier.
- Identification des compétences documentées du profil.
- Calcul des correspondances entre profil et métier.
- Identification des compétences non documentées.
- Distinction entre absence de preuve et absence de maîtrise.
- Génération de recommandations personnalisées.
- Justification à partir des offres et relations ESCO.
- Présentation des sources utilisées.
- Gestion des cas où les preuves sont insuffisantes.
- Évaluation de la fidélité des recommandations.

**Séance cible :** S4–S5

**Responsables :** Essaied Nour / Trabelsi Nidhal

---

## 3. SHOULD HAVE — Forte valeur ajoutée industrielle

### US-09 — Tracing MLOps Distribué

**User Story :**

En tant que responsable IA, je veux tracer les différentes
étapes du pipeline GraphRAG afin d'identifier les
problèmes de performance et les erreurs.

**Critères d'acceptation :**

- Intégration de Langfuse ou OpenTelemetry.
- Tracing des embeddings.
- Tracing de la recherche vectorielle.
- Tracing du reranking.
- Tracing des appels LLM.
- Mesure des latences par étape.
- Suivi de la consommation de tokens.
- Journalisation sans exposition de données sensibles.

**Séance cible :** S3–S4

**Responsable :** Essaied Nour

---

### US-10 — Cache Sémantique Redis

**User Story :**

En tant qu'architecte système, je veux réutiliser
les résultats de requêtes similaires afin de
réduire la latence et les coûts de génération.

**Critères d'acceptation :**

- Intégration de Redis.
- Seuil de similarité cosinus > 0,95.
- Réponse issue du cache en moins de 50 ms.
- Invalidation des entrées obsolètes.
- Séparation des données entre utilisateurs.
- Respect de la confidentialité des profils.

**Séance cible :** S4

**Responsable :** Essaied Nour

---

### US-11 — Évaluation Continue avec Ragas

**User Story :**

En tant que Data Scientist, je veux évaluer régulièrement
les réponses de PathForge AI afin de suivre la qualité
du système au cours des itérations.

**Critères d'acceptation :**

- Création d'un benchmark de référence annoté.
- Calcul automatisé de Faithfulness.
- Calcul d'Answer Relevance.
- Évaluation de la qualité du retrieval.
- Comparaison entre RAG hybride et GraphRAG hybride.
- Conservation des rapports d'évaluation.
- Suivi des évolutions de performance.

**Séance cible :** S3–S6

**Responsables :** Fourati Yosr / Essaied Nour

---

## 4. COULD HAVE — Différenciateurs Optionnels

### US-12 — Déploiement Kubernetes

**User Story :**

En tant qu'ingénieur DevOps, je veux déployer PathForge AI
sur Kubernetes afin de faciliter la gestion des services.

**Critères d'acceptation :**

- Manifests Kubernetes fonctionnels.
- Deployments et Services.
- ConfigMaps et Secrets.
- Ingress.
- Horizontal Pod Autoscaler.
- Documentation du déploiement.

**Responsable :** Trabelsi Nidhal

---

### US-13 — Routage Agentique Multi-Outils

**User Story :**

En tant qu'utilisateur, je veux que le système sélectionne
automatiquement le moteur adapté à ma question.

**Critères d'acceptation :**

- Routage entre recherche documentaire Qdrant.
- Exploration du graphe Neo4j.
- Requêtes SQL autorisées sur PostgreSQL.
- Contrôle des accès aux outils.
- Journalisation des décisions de routage.

**Responsable :** Essaied Nour

---

### US-14 — Support Multimodal

**User Story :**

En tant qu'étudiant, je veux importer des documents
scannés ou contenant des tableaux afin que PathForge
puisse exploiter davantage de sources.

**Critères d'acceptation :**

- Extraction OCR des documents scannés.
- Reconnaissance des tableaux.
- Conservation des métadonnées.
- Indexation des contenus extraits.
- Évaluation sur des documents de référence.

**Responsable :** Trabelsi Nidhal

---

## 5. WON'T HAVE — Exclus du Périmètre

Les fonctionnalités suivantes ne seront pas développées
dans la première version du projet :

- Entraînement complet d'un LLM depuis zéro.
- Développement d'une plateforme SaaS avec facturation.
- Intégration de paiements Stripe.
- Application mobile native Android ou iOS.
- Candidatures automatiques aux offres d'emploi.
- Plateforme complète de recrutement.
- Classement automatique des candidats pour les entreprises.
- Garantie d'embauche ou certification automatique
  de la maîtrise des compétences.

---

## 6. Métriques de Réussite

Les objectifs suivants permettront d'évaluer
la qualité du moteur PathForge AI.

| Métrique | Objectif cible |
|---|---|
| Recall@10 | >= 85 % |
| Recall@5 | >= 80 % |
| Faithfulness (Ragas) | >= 0,85 |
| Answer Relevance | >= 0,80 |
| Time-to-First-Token | < 800 ms |
| Latence E2E P95 | < 3,5 s |

Des métriques complémentaires seront utilisées :

- Précision d'extraction des compétences.
- Rappel d'extraction des compétences.
- Exactitude de la normalisation ESCO.
- NDCG@10 pour le classement des offres.
- Qualité des relations du graphe.
- Proportion des recommandations accompagnées de sources.

Les performances seront évaluées sur un
jeu de données de référence annoté.

Ces seuils sont des objectifs prévisionnels
et non des résultats déjà obtenus.

---

## 7. Critères de Réussite du Projet

La livraison finale devra démontrer :

1. Une ingestion fonctionnelle des données ESCO,
   des offres d'emploi et des profils étudiants.
2. Une recherche hybride BM25 + embeddings.
3. Un reranking améliorant la sélection des résultats.
4. Une extraction et normalisation des compétences.
5. Un graphe Neo4j reliant projets, compétences et métiers.
6. Une analyse explicable des écarts de compétences.
7. Des recommandations personnalisées et sourcées.
8. Une API FastAPI et une interface React fonctionnelles.
9. Des évaluations quantitatives reproductibles.
10. Un déploiement Docker et un pipeline CI/CD opérationnels.

---

## 8. État d'Avancement

### Livrables déjà réalisés

- [x] Dépôt GitHub structuré.
- [x] Fiche de cadrage d'ingénierie.
- [x] Architecture initiale GraphRAG.
- [x] Choix de la base vectorielle Qdrant.
- [x] Documentation du backlog MoSCoW.
- [x] Dataset ESCO v1.2.1 préparé.
- [x] Sous-ensemble de 674 relations ESCO validé.
- [x] Script de validation des relations ESCO.
- [x] Docker Compose pour Qdrant.
- [x] Démarrage local du dashboard Qdrant.

### Travaux prévus

- [ ] Préparation du corpus d'offres d'emploi.
- [ ] Constitution des profils étudiants fictifs.
- [ ] Pipeline d'ingestion et de chunking.
- [ ] Indexation vectorielle des documents.
- [ ] Recherche hybride et reranking.
- [ ] Construction du graphe Neo4j.
- [ ] Développement des endpoints FastAPI.
- [ ] Développement de l'interface React.
- [ ] Intégration du LLM.
- [ ] Évaluation Ragas.
- [ ] Tests automatisés et CI/CD.
- [ ] Déploiement final multi-services.

---

## 9. Répartition des Responsabilités

| Membre | Domaine | User Stories principales |
|---|---|---|
| Fourati Yosr | Data / Retrieval | US-01, US-02, US-03, US-15 |
| Essaied Nour | Backend / MLOps | US-04, US-05, US-07, US-17 |
| Trabelsi Nidhal | Frontend / Infra | US-06, US-08, US-12, US-14 |

Les US-09, US-10, US-11, US-13 et US-16
seront réalisées en collaboration selon les besoins.

Les responsabilités pourront évoluer au cours du projet.

---

## 10. Conclusion

Ce backlog MoSCoW définit une feuille de route
technique progressive pour PathForge AI.

Il associe les exigences d'ingénierie du moteur RAG
aux fonctionnalités métier spécifiques de la plateforme.

La priorité est de disposer d'un système capable
d'identifier les compétences documentées des étudiants,
de les comparer aux exigences professionnelles
et de proposer des recommandations explicables
à partir de sources vérifiables.
