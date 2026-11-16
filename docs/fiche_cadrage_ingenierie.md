# Fiche de Cadrage d'Ingénierie — Projet Fédérateur AI-BD_BI

## Spécification du Moteur RAG / Data Intelligent

**Projet : PathForge AI**

*Plateforme intelligente d'analyse des compétences et d'accompagnement à l'orientation professionnelle par GraphRAG hybride*

---

## 1. Fiche d'Identité du Projet

**Nom du projet :** PathForge AI

**Domaine d'application :** Intelligence artificielle, Big Data, orientation professionnelle et analyse des compétences.

**Membres de l'équipe :**

| Membre | Responsabilité principale |
|---|---|
| Fourati Yosr | Lead Data / Retrieval |
| Essaied Nour | Lead Backend / MLOps |
| Trabelsi Nidhal | Lead Frontend / Infra |

**Lien du dépôt GitHub :** https://github.com/nouressaied/PathForge-AI

**Branche principale :** `main` — protection à configurer.

**Nature de la solution :** Application web intelligente intégrant un moteur de recherche hybride, un graphe de connaissances et un modèle de langage pour générer des recommandations personnalisées et explicables.

---

## 2. Cadrage du Problème Métier — « Problem-First »

### 2.1 Persona cible et contexte opérationnel

**Utilisateur visé :**

Le principal utilisateur de PathForge AI est un étudiant universitaire, particulièrement en fin de cursus, qui souhaite identifier les compétences nécessaires pour accéder à un métier donné et préparer efficacement son insertion professionnelle.

La plateforme cible initialement les étudiants en informatique, intelligence artificielle, Data Science et Big Data.

**Contexte opérationnel :**

Au cours de leur formation, les étudiants développent différentes compétences à travers les enseignements universitaires, les stages, les certifications et les projets académiques.

Toutefois, ces expériences sont généralement présentées dans des documents distincts : CV, portfolios, rapports de projets et attestations.

Parallèlement, les exigences professionnelles sont dispersées entre les offres d'emploi, les descriptions de postes et les référentiels de compétences.

Cette fragmentation complique l'identification des correspondances entre le profil réel d'un étudiant et les compétences nécessaires pour exercer un métier.

**Point de douleur majeur (Pain Point) :**

Un étudiant peut maîtriser plusieurs technologies sans savoir précisément :

- Si ses compétences correspondent aux exigences du métier qu'il souhaite exercer.
- Quelles compétences sont déjà documentées par ses projets et stages.
- Quelles compétences restent à acquérir ou à démontrer.
- Pourquoi certaines technologies sont nécessaires pour un métier donné.
- Quelles actions concrètes pourraient améliorer son adéquation avec le profil recherché.

**Exemple concret :**

Un étudiant souhaite devenir *GenAI Engineer*. Il possède une expérience en Python, FastAPI et NLP, démontrée par ses projets universitaires.

Cependant, certaines offres d'emploi requièrent également des compétences en RAG avancé, évaluation des LLM, Docker ou MLOps.

L'étudiant doit alors consulter manuellement plusieurs annonces, comparer les exigences avec son CV et déterminer les compétences à approfondir.

**Limites des approches classiques — Pourquoi l'IA générative ?**

Les méthodes traditionnelles de correspondance CV–emploi reposent souvent sur des mots-clés ou des critères préétablis.

Elles présentent plusieurs limites :

- Difficulté à reconnaître les compétences formulées avec des expressions différentes.
- Faible exploitation des liens entre projets, technologies et métiers.
- Absence de justification détaillée des correspondances proposées.
- Difficulté à synthétiser des exigences issues de plusieurs documents.
- Recommandations parfois génériques et insuffisamment contextualisées.

L'utilisation d'une architecture GraphRAG hybride vise à dépasser ces limites en associant la compréhension sémantique des documents et l'exploitation explicite des relations entre compétences et métiers.

### 2.2 Proposition de valeur

**Problématique :**

Comment exploiter et relier intelligemment les compétences documentées des étudiants, leurs expériences académiques et professionnelles et les exigences du marché de l'emploi afin de proposer un parcours d'évolution professionnelle personnalisé, pertinent et explicable ?

**Solution proposée :**

PathForge AI est une plateforme d'aide à l'orientation professionnelle reposant sur une architecture GraphRAG hybride.

Le système analysera les CV, les projets et les expériences des étudiants afin d'identifier les compétences déclarées et documentées.

Il exploitera ensuite le référentiel ESCO et un corpus d'offres d'emploi pour déterminer les compétences associées aux métiers ciblés.

À travers la recherche hybride et un graphe de connaissances, la plateforme pourra rapprocher ces différentes informations, identifier les écarts et générer des recommandations justifiées par des sources.

**Valeur ajoutée :**

Contrairement à un simple moteur de recommandation d'emplois, PathForge AI cherchera à expliquer :

1. Quelles compétences sont documentées par les expériences de l'étudiant.
2. Quelles compétences sont exigées pour le métier cible.
3. Quels écarts sont identifiés.
4. Quelles preuves justifient ces correspondances.
5. Quelles actions peuvent contribuer à améliorer le profil.

L'objectif n'est donc pas uniquement de recommander un métier, mais d'aider l'étudiant à comprendre comment s'y préparer.

---

## 3. Données et Volumétrie

### 3.1 Formats des données sources

- [x] **PDF :** CV et descriptions de projets étudiants.
- [x] **CSV / JSON :** référentiel ESCO, offres d'emploi et profils de démonstration.
- [ ] **Tables relationnelles SQL :** stockage applicatif prévu avec PostgreSQL.
- [ ] **Markdown :** ressources pédagogiques complémentaires éventuelles.
- [ ] **Images / Scans :** traitement multimodal exclu du premier prototype.

### 3.2 Sources de données

**Source 1 — ESCO v1.2.1**

Référentiel européen officiel décrivant les métiers, les compétences et les relations entre ces concepts.

Source : https://esco.ec.europa.eu/en/use-esco/download

Le corpus actuellement préparé comprend :

| Fichier | Contenu |
|---|---|
| `occupations_en.csv` | 3 043 métiers |
| `skills_en.csv` | 13 960 compétences |
| `occupationSkillRelations_data_ai_en.csv` | 674 relations filtrées |

Le sous-ensemble des relations concerne huit métiers orientés Data, IA et développement logiciel.

Un script Python a permis de vérifier la cohérence référentielle des 674 relations : aucune référence à un métier ou une compétence inconnue n'a été détectée.

**Source 2 — LinkedIn Job Postings (2023–2024), Kaggle**

Corpus historique d'offres d'emploi contenant notamment les intitulés des postes, des descriptions et des informations professionnelles.

Source : https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

Ce dataset permettra d'étudier les compétences demandées dans les offres d'emploi et de compléter les relations métiers-compétences du référentiel ESCO.

Les offres étant historiques, elles ne seront pas présentées comme une représentation actualisée du marché.

**Source 3 — Profils étudiants fictifs ou anonymisés**

Corpus constitué par l'équipe pour évaluer l'extraction et l'analyse des compétences.

Chaque profil pourra contenir des informations sur les formations, les projets, les stages, les technologies utilisées et le métier cible.

### 3.3 Volumétrie initiale — PoC S1 à S3

| Corpus | Volumétrie initiale |
|---|---|
| ESCO | 3 043 métiers, 13 960 compétences, 674 relations filtrées |
| Offres d'emploi | 100 à 200 offres ciblées Data/IA |
| Profils étudiants | 10 à 20 profils fictifs |
| Documents indexés | Environ 500 à 2 000 chunks prévus |

Les volumes d'offres, de profils et de chunks constituent des objectifs prévisionnels.

### 3.4 Volumétrie cible du prototype final

- 500 à 1 000 offres d'emploi.
- 30 à 50 profils étudiants.
- Référentiel ESCO enrichi par les relations pertinentes.
- Environ 5 000 à 15 000 chunks indexés, selon la stratégie d'ingestion retenue.

Ces estimations seront ajustées après les premières expérimentations.

### 3.5 Fréquence de mise à jour

- [x] **Statique :** corpus initial figé pour les premières expérimentations.
- [ ] **Batch quotidien :** extension envisagée pour intégrer de nouvelles offres.
- [ ] **Temps réel / Streaming :** non retenu pour l'ingestion du premier prototype.

---

## 4. Architecture Technique et Composants RAG

### 4.1 Architecture générale

PathForge AI reposera sur une architecture **GraphRAG hybride**, associant un moteur de recherche documentaire, une base vectorielle, un graphe de connaissances et un LLM.

Le traitement se déroulera en plusieurs étapes :

**1. Ingestion des données**

Extraction, nettoyage et normalisation des informations issues des CV, des descriptions de projets, du référentiel ESCO et des offres d'emploi.

**2. Prétraitement et indexation**

Découpage des documents textuels en chunks, génération d'embeddings et indexation dans Qdrant.

Les données relationnelles ESCO seront conservées dans une structure adaptée à leur exploitation dans Neo4j.

**3. Recherche hybride**

Combinaison d'une recherche lexicale BM25 et d'une recherche sémantique fondée sur les embeddings.

Les résultats seront ensuite fusionnés et réordonnés grâce à un Cross-Encoder.

**4. Exploration du graphe de connaissances**

Neo4j permettra d'explorer les relations entre les étudiants, leurs projets, les compétences identifiées, les offres d'emploi et les métiers.

**5. Génération augmentée**

Le LLM recevra les passages documentaires pertinents ainsi que les relations validées du graphe pour produire une analyse personnalisée et sourcée.

**6. Restitution**

Les recommandations seront accessibles à travers une interface React connectée à un backend FastAPI.

### 4.2 Stratégie de chunking

**Stratégie retenue :** Recursive Character Chunking pour les CV et les descriptions d'offres.

**Taille visée :** 512 tokens.

**Overlap :** 64 tokens.

Les identifiants de documents et métadonnées seront préservés afin de permettre la traçabilité des informations.

Les relations ESCO ne seront pas découpées en chunks textuels, mais traitées comme des données structurées.

### 4.3 Modèles et outils de recherche

**Modèle d'embeddings envisagé :** `BAAI/bge-m3`

**Dimension dense :** 1 024 dimensions.

**Base vectorielle retenue :** Qdrant.

**Justification :**

Qdrant a été retenu pour ses fonctionnalités de recherche vectorielle, sa prise en charge des vecteurs denses et sparse, ses possibilités de filtrage par métadonnées et sa simplicité de déploiement via Docker Compose.

Une instance Qdrant v1.15.5 a déjà été démarrée localement et son interface web a été vérifiée.

**Recherche hybride :** BM25 + embeddings, avec fusion des résultats.

**Reranker envisagé :** `BAAI/bge-reranker-v2-m3`.

### 4.4 Graphe de connaissances — Neo4j

Le graphe représentera notamment les relations suivantes :

- Étudiant → RÉALISE → Projet
- Projet → DOCUMENTE → Compétence
- Métier → REQUIERT → Compétence
- Offre → MENTIONNE → Compétence
- Étudiant → CIBLE → Métier

La normalisation des compétences s'appuiera sur les identifiants ESCO lorsque les correspondances pourront être justifiées.

### 4.5 Génération et application

**LLM envisagé :** modèle instruct multilingue, à sélectionner après évaluation. Qwen via Ollama constitue une option locale.

**Orchestration :** LangChain ou LlamaIndex.

**Backend :** FastAPI et Pydantic v2.

**Frontend :** React.

**Base relationnelle :** PostgreSQL.

**Conteneurisation :** Docker Compose.

**Intégration continue :** GitHub Actions.

Le choix définitif du LLM et les performances de l'architecture seront validés expérimentalement.

---

## 5. Métriques Quantitatives et SLAs

L'évaluation portera sur la qualité de la recherche documentaire, la fiabilité des réponses et les performances du système.

| Métrique | Définition / Outil | Objectif cible |
|---|---|---|
| Recall@10 | Proportion de documents pertinents retrouvés dans le Top 10 | ≥ 85 % |
| Faithfulness — Ragas | Fidélité des réponses aux documents récupérés | ≥ 0,85 |
| Answer Relevance — Ragas | Pertinence des réponses générées par rapport aux questions | ≥ 0,80 |
| Latence First-Token (TTFT) | Temps d'affichage du premier token en streaming | < 800 ms |
| Latence E2E P95 | Temps total de réponse au 95e percentile | < 3,5 s |

**Évaluation complémentaire propre à PathForge AI :**

- Précision de l'extraction des compétences depuis les CV.
- Exactitude de la normalisation des compétences avec ESCO.
- NDCG@10 pour évaluer le classement des offres.
- Exactitude des relations métiers-compétences exploitées.
- Traçabilité des recommandations générées.

**Protocole d'évaluation envisagé :**

Constitution d'un jeu de questions de référence accompagné de documents pertinents, de correspondances de compétences validées et de résultats attendus.

Les expérimentations permettront de comparer la recherche lexicale, la recherche sémantique, la recherche hybride et l'approche GraphRAG.

Les objectifs annoncés constituent des seuils de performance à atteindre, et non des résultats déjà obtenus.

---

## 6. Gestion des Risques et Garde-fous

### 6.1 Prévention des hallucinations

Le LLM devra fonder ses réponses sur les documents récupérés et les relations validées du graphe.

En l'absence de preuve suffisante, il devra indiquer explicitement que les données disponibles ne permettent pas de conclure.

Les recommandations seront accompagnées des références utilisées.

### 6.2 Fiabilité de l'analyse des compétences

La plateforme distinguera :

- Les compétences déclarées par l'étudiant.
- Les compétences documentées par ses projets ou expériences.
- Les compétences dont la maîtrise ne peut pas être déterminée à partir des informations disponibles.

Une compétence absente du CV ne sera pas automatiquement considérée comme non maîtrisée.

### 6.3 Protection des données personnelles

Le dépôt GitHub public utilisera exclusivement des profils fictifs ou des données suffisamment anonymisées et autorisées.

Les CV réels nécessiteront le consentement des personnes concernées, des contrôles d'accès et une politique adaptée de conservation des données.

### 6.4 Protection des secrets

Les clés API, mots de passe et paramètres sensibles seront stockés dans des variables d'environnement.

Les fichiers `.env` contenant des secrets seront exclus du suivi Git.

### 6.5 Isolation réseau

Qdrant, Neo4j et PostgreSQL seront configurés dans des réseaux Docker internes lorsque l'architecture complète sera déployée.

Seuls les services nécessaires seront exposés.

### 6.6 Limites de la solution

PathForge AI restera un outil d'aide à l'orientation professionnelle.

La plateforme ne devra pas garantir l'obtention d'un emploi, certifier automatiquement la maîtrise d'une compétence ou produire des décisions définitives sur l'employabilité d'un étudiant.

Son objectif sera de fournir des recommandations contextualisées, explicables et vérifiables afin d'accompagner l'étudiant dans son évolution professionnelle.
