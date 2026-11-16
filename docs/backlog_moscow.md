# Backlog Technique MoSCoW — PathForge AI

## Découpage Agile des User Stories & Critères d'Acceptation

### 1. MUST HAVE — Indispensables pour la livraison finale S7

| ID | User Story technique adaptée à PathForge | Critères d'acceptation (DoD) | Séance |
|---|---|---|---|
| US-01 | **Ingestion et chunking structuré :** En tant que Data Engineer, je veux ingérer les offres, les CV et le référentiel ESCO pour préparer leur exploitation. | Script Python asynchrone avec gestion des erreurs ; métadonnées `doc_id`, `source`, `chunk_id`, `job_id` ou `profile_id` ; conservation des relations structurées ESCO. | S2 |
| US-02 | **Indexation vectorielle HNSW :** En tant que moteur RAG, je veux indexer les offres et descriptions de compétences pour permettre la recherche sémantique. | Qdrant démarré via Docker ; index HNSW avec distance Cosine ; insertion de lots de 64 chunks avec temps cible inférieur à 50 ms, à mesurer. | S2 |
| US-03 | **Retrieval hybride et reranking :** En tant qu'étudiant, je veux retrouver les compétences et offres pertinentes même si les formulations diffèrent. | Fusion BM25 + recherche dense ; top-20 initial ; Cross-Encoder sélectionnant le top-5 ; Recall@5 ≥ 80 % sur un jeu annoté. | S3 |
| US-04 | **API REST FastAPI :** En tant qu'application cliente, je veux interroger le moteur d'analyse de compétences. | Schémas Pydantic v2 ; endpoints de recherche et d'analyse ; validation des entrées ; HTTP 422 pour données invalides ; documentation Swagger. | S4 |
| US-05 | **Génération de réponses en streaming SSE :** En tant qu'étudiant, je veux obtenir progressivement une explication de mes écarts de compétences. | Endpoint `/api/v1/chat/stream` ; événements SSE ; sources associées aux recommandations ; objectif TTFT < 800 ms. | S4–S5 |
| US-06 | **Interface web réactive :** En tant qu'étudiant, je veux sélectionner un métier et visualiser mes compétences, les écarts et les recommandations. | Interface React ; formulaire de profil ; métier cible ; résultats sourcés ; gestion des chargements et erreurs ; aucune actualisation complète de page. | S5 |
| US-07 | **Assurance qualité et CI/CD :** En tant que développeur, je veux détecter automatiquement les régressions du système. | Au moins 4 tests Pytest avec mocks LLM et Qdrant ; Ruff ; workflow GitHub Actions fonctionnel ; contrôles de fusion configurés. | S6 |
| US-08 | **Conteneurisation de production :** En tant qu'ingénieur DevOps, je veux déployer PathForge de manière reproductible. | Dockerfiles multi-stage ; processus non-root ; Docker Compose multi-services ; secrets via variables d'environnement ; tests de démarrage réussis. | S7 |

**Exigence métier transversale :** L'analyse des écarts devra distinguer les compétences déclarées, les compétences documentées et celles sans preuve suffisante. Les recommandations devront être liées aux offres ou aux relations ESCO qui les justifient.

### 2. SHOULD HAVE — Forte valeur ajoutée industrielle

| ID | User Story | Critères d'acceptation | Séance |
|---|---|---|---|
| US-09 | **Tracing MLOps :** Suivre les différentes étapes d'une requête PathForge avec Langfuse ou OpenTelemetry. | Traces d'embedding, recherche, reranking et LLM ; latences par étape ; consommation de tokens. | S3–S4 |
| US-10 | **Cache sémantique Redis :** Réutiliser certaines réponses pour réduire le temps de génération. | Similarité cosinus > 0,95 ; réponse en cache < 50 ms ; invalidation lors de la modification des données pertinentes. | S4 |
| US-11 | **Évaluation continue Ragas :** Mesurer la qualité des explications sur un benchmark de référence. | Calcul automatisé de Faithfulness et Answer Relevance ; résultats comparables entre versions. | S3 |

### 3. COULD HAVE — Différenciateurs optionnels

| ID | User Story | Critères d'acceptation |
|---|---|---|
| US-12 | **Déploiement Kubernetes :** Préparer une version orchestrée de PathForge. | Manifests Deployment, Service, ConfigMap, Ingress et HPA fonctionnels. |
| US-13 | **Routage agentique multi-outils :** Diriger les requêtes vers le bon moteur selon leur intention. | Routage entre recherche documentaire Qdrant, exploration Neo4j et requêtes SQL autorisées. |
| US-14 | **Support multimodal :** Analyser des CV scannés et des tableaux présents dans des documents. | Extraction OCR, conservation des tableaux et tests sur documents multimodaux. |

### 4. WON'T HAVE — Exclus du périmètre

- Entraînement d'un LLM de grande taille depuis zéro.
- Plateforme SaaS avec abonnement et paiement.
- Application mobile native Android ou iOS.
- Candidatures automatiques aux offres d'emploi.
- Recrutement ou classement automatique des étudiants par les entreprises.

### 5. Critères de réussite du projet

La livraison finale devra démontrer :

- Une ingestion fonctionnelle des corpus ESCO, offres d'emploi et profils étudiants.
- Une recherche hybride avec reranking évaluée quantitativement.
- Un graphe de connaissances reliant métiers, compétences et projets.
- Une analyse des écarts de compétences à partir de preuves documentées.
- Une réponse générée avec des références vérifiables.
- Une application FastAPI et React fonctionnelle.
- Un déploiement Docker reproductible et un pipeline de tests automatisés.

Les fonctionnalités Should Have et Could Have seront réalisées selon l'avancement de l'équipe, après validation des fonctionnalités indispensables.
