# Fiche de Cadrage d'Ingénierie — Projet Fédérateur AI-BD_BI

## Spécification du Moteur RAG / Data Intelligent

### 1. Fiche d'Identité du Projet

**Nom du projet :** PathForge AI — Plateforme intelligente d'analyse des compétences et d'orientation professionnelle par GraphRAG hybride.

**Membres de l'équipe :**
1. [Fourati Yosr] — Lead Data / Retrieval
2. [Essaied Nour] — Lead Backend / MLOps
3. [Trabelsi Nidhal] — Lead Frontend / Infra

**Dépôt GitHub :** https://github.com/nouressaied/PathForge-AI

**Branche principale :** `main` — protection à configurer.

---

### 2. Cadrage du Problème Métier (Problem-First)

#### 2.1 Persona cible et contexte opérationnel

**Utilisateur visé :** Étudiant universitaire, notamment en dernière année, souhaitant identifier les compétences nécessaires pour atteindre un métier cible.

**Point de douleur majeur :** Les étudiants possèdent des connaissances, projets et expériences de stage, mais rencontrent des difficultés à relier leurs compétences aux attentes réelles des entreprises et à identifier les compétences qu'ils doivent développer.

**Limites des approches classiques :** Les comparateurs de CV et les recherches par mots-clés ne permettent pas toujours de reconnaître les compétences exprimées différemment, de relier les projets aux compétences qu'ils documentent ou d'expliquer les écarts entre un profil et un métier.

#### 2.2 Proposition de valeur

Développer une plateforme GraphRAG hybride qui analyse les CV et projets étudiants, retrouve les exigences des métiers à partir d'ESCO et des offres d'emploi, puis construit des recommandations personnalisées, explicables et appuyées par des sources vérifiables.

**Valeur ajoutée :** Passer d'une simple correspondance CV–emploi à une analyse argumentée des compétences documentées, des écarts identifiés et des actions permettant d'atteindre un métier cible.

---

### 3. Données et Volumétrie

**Formats des données sources :**
- [x] PDF : CV et descriptions de projets.
- [x] JSON / CSV : référentiel ESCO, offres d'emploi et profils étudiants.
- [ ] Tables relationnelles SQL : stockage applicatif prévu.
- [ ] Markdown : ressources pédagogiques éventuelles.
- [ ] Images / scans : hors périmètre du premier prototype.

**Sources principales :**

1. **ESCO v1.2.1** — Référentiel officiel des métiers et compétences.
   https://esco.ec.europa.eu/en/use-esco/download

2. **LinkedIn Job Postings (2023–2024) — Kaggle** — Corpus historique d'offres professionnelles.
   https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

3. **Profils étudiants fictifs ou anonymisés** — Corpus constitué par l'équipe pour tester l'extraction des compétences et les recommandations.

**Volumétrie initiale (PoC S1–S3) :**
- Référentiel ESCO : trois fichiers CSV principaux (métiers, compétences, relations).
- 100 à 200 offres d'emploi sélectionnées dans les domaines Data et IA.
- 10 à 20 profils étudiants fictifs.
- Environ 500 à 2 000 passages indexés, selon la stratégie de découpage retenue.

**Volumétrie cible du prototype final :**
- 500 à 1 000 offres d'emploi.
- 30 à 50 profils étudiants fictifs ou consentis.
- Ensemble pertinent des métiers et compétences ESCO.
- Environ 5 000 à 15 000 passages indexés, à confirmer après analyse des données.

Ces volumes sont des objectifs prévisionnels, non des corpus déjà entièrement constitués.

**Fréquence de mise à jour :**
- [x] Statique : première version basée sur les datasets téléchargés.
- [ ] Batch quotidien : évolution possible avec une source d'offres actualisées.
- [ ] Temps réel / Streaming : non retenu pour le MVP.

---

### 4. Architecture Technique et Composants RAG

**Stratégie de chunking retenue :** Recursive Character Chunking pour les descriptions d'offres et les documents textuels.

**Traitement spécifique :** Les tables et relations ESCO seront conservées sous forme structurée et ne seront pas découpées comme des paragraphes ordinaires.

**Taille de chunk visée :** 512 tokens.

**Overlap :** 64 tokens.

**Modèle d'embeddings envisagé :** BAAI/bge-m3.

**Dimension des vecteurs denses :** 1024.

**Base vectorielle retenue :** Qdrant.

**Justification :** Recherche vectorielle dense et sparse, filtrage par métadonnées, intégration Python/FastAPI et déploiement local simple avec Docker Compose. La latence sera mesurée expérimentalement.

**Recherche hybride :** BM25 + embeddings, avec fusion des résultats et reranking.

**Reranker envisagé :** BAAI/bge-reranker-v2-m3, Cross-Encoder multilingue.

**Graphe de connaissances :** Neo4j.

**Relations principales :**
- Étudiant → réalise → Projet
- Projet → documente → Compétence
- Métier → requiert → Compétence
- Offre → mentionne → Compétence

Les compétences extraites seront normalisées à l'aide du référentiel ESCO lorsque les correspondances sont suffisamment fiables.

**LLM de génération :** Modèle instruct multilingue à sélectionner après tests de qualité, de latence et de compatibilité matérielle. Un modèle Qwen via Ollama constitue une option pour le prototype local.

**Orchestration :** LangChain ou LlamaIndex.

**Backend :** FastAPI + Pydantic v2.

**Frontend :** React.

**Base relationnelle :** PostgreSQL.

**Déploiement :** Docker Compose avec intégration continue GitHub Actions.

---

### 5. Métriques Quantitatives et SLAs

| Métrique | Méthode d'évaluation | Objectif cible |
|---|---|---|
| Recall@10 | Proportion de références pertinentes retrouvées dans les 10 premiers résultats | ≥ 85 % |
| Faithfulness (Ragas) | Fidélité des réponses aux sources fournies | ≥ 0,85 |
| Answer Relevance (Ragas) | Pertinence des réponses par rapport aux questions | ≥ 0,80 |
| Latence First-Token (TTFT) | Délai jusqu'au premier token généré en streaming | < 800 ms |
| Latence E2E P95 | Temps total de réponse au 95e percentile | < 3,5 s |

**Métriques complémentaires propres à PathForge :**
- Précision et rappel de l'extraction des compétences.
- NDCG@10 pour le classement des offres.
- Exactitude des correspondances entre compétences et identifiants ESCO.
- Proportion des recommandations accompagnées de preuves vérifiables.

Les objectifs de latence et de qualité devront être vérifiés avec un benchmark annoté et sur l'environnement matériel réellement utilisé.

---

### 6. Gestion des Risques et Garde-fous

**Prévention des hallucinations :** Le LLM doit générer les recommandations uniquement à partir des compétences extraites, des offres indexées et des relations vérifiées. En l'absence de preuve suffisante, la plateforme devra l'indiquer explicitement.

**Distinction entre compétence déclarée et démontrée :** Une compétence mentionnée dans un CV ne sera pas automatiquement considérée comme maîtrisée.

**Protection des données personnelles :** Utilisation de profils fictifs ou anonymisés dans le dépôt public. Les CV réels nécessitent le consentement des personnes concernées, un traitement limité aux besoins du projet et des contrôles d'accès.

**Protection des secrets :** Utilisation de variables d'environnement dans `.env`, exclusion du fichier de Git et absence de clés API dans le code source.

**Isolation réseau :** Qdrant, Neo4j et PostgreSQL seront configurés sur un réseau Docker interne. Les services seront exposés uniquement lorsque nécessaire.

**Contrôle des recommandations :** Chaque correspondance devra être accompagnée de ses sources et de son niveau de justification. PathForge restera un outil d'aide à l'orientation, et non un outil de décision automatique sur les compétences ou l'employabilité d'une personne.
