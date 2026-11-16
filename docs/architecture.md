
# Architecture Technique — PathForge AI

## 1. Présentation générale

**PathForge AI** est une plateforme intelligente d'analyse des
compétences et d'orientation professionnelle reposant sur une
architecture **GraphRAG hybride**.

Elle analyse les compétences documentées par les CV, projets
et stages des étudiants, puis les compare aux compétences
exigées pour un métier cible.

Son objectif est de proposer des recommandations
personnalisées, explicables et justifiées par des sources.

### Technologies principales

| Composant | Technologie | Rôle |
|---|---|---|
| Recherche hybride | BM25 + embeddings | Recherche lexicale et sémantique |
| Base vectorielle | Qdrant | Indexation et récupération de documents |
| Reranking | Cross-Encoder | Reclassement des résultats |
| Graphe de connaissances | Neo4j | Relations entre compétences et métiers |
| Génération | LLM | Explications et recommandations sourcées |
| Backend | FastAPI, Pydantic v2 | API et orchestration |
| Frontend | React | Interface étudiant |
| Base relationnelle | PostgreSQL | Profils et historiques |
| Évaluation | Ragas | Qualité des réponses |
| Déploiement | Docker Compose | Exécution des services |

L'architecture comprend deux pipelines complémentaires :

1. **Pipeline d'ingestion :** préparation et indexation des données.
2. **Pipeline GraphRAG :** recherche, analyse des écarts et génération.

---

## 2. Schéma d'architecture générale

### Architecture GraphRAG hybride — Vue d'ensemble

**ÉTAPE 1 — SOURCES DE DONNÉES**

| CV et projets | Offres d'emploi | Référentiel ESCO |
|---|---|---|
| Compétences documentées | Compétences recherchées | Métiers et relations |

**↓**

**ÉTAPE 2 — INGESTION ET PRÉTRAITEMENT**

Extraction → Nettoyage → Normalisation ESCO → Chunking → Embeddings

**↓**

**ÉTAPE 3 — STOCKAGE ET INDEXATION**

| Qdrant | Neo4j | PostgreSQL |
|---|---|---|
| Index dense et sparse | Graphe de connaissances | Données applicatives |
| Recherche hybride | Relations métiers-compétences | Profils et historiques |
| Filtrage par métadonnées | Chemins de preuves | Gestion des informations |

**↓**

**ÉTAPE 4 — MOTEUR GRAPHRAG**

| Composant | Traitement |
|---|---|
| FastAPI | Orchestration des requêtes |
| Qdrant | Recherche hybride BM25 + embeddings |
| Cross-Encoder | Fusion et reranking des résultats |
| Neo4j | Exploration des relations du graphe |
| Construction du contexte | Regroupement des documents et des preuves |
| LLM | Génération de recommandations sourcées |

**↓**

**ÉTAPE 5 — RÉSULTATS PERSONNALISÉS**

| Analyse | Résultat |
|---|---|
| Profil étudiant | Compétences documentées |
| Métier cible | Compétences exigées |
| Comparaison | Écarts identifiés |
| Recommandations | Actions suggérées avec sources |

**↓**

**ÉTAPE 6 — INTERFACE UTILISATEUR**

**React — PathForge AI**

Import du CV → Sélection du métier → Analyse → Recommandations

**Évaluation transversale :** Ragas, Recall@10,
Faithfulness, Answer Relevance et mesures de latence.

### Fonctionnement des deux pipelines

**Pipeline d'ingestion :**

Les données sources sont extraites, nettoyées et normalisées.

Les documents textuels sont découpés et vectorisés
avant leur indexation dans Qdrant.

Les relations structurées entre métiers et compétences
sont préparées pour leur exploitation dans Neo4j.

**Pipeline de recherche et génération :**

L'étudiant sélectionne un métier cible depuis React.

FastAPI orchestre la recherche hybride dans Qdrant
et l'exploration des relations Neo4j.

Les informations retrouvées sont regroupées
dans un contexte transmis au LLM.

Le système produit une analyse des écarts
et des recommandations accompagnées de sources.

---

## 3. Sources de données

### 3.1 Référentiel ESCO

**Source :**
https://esco.ec.europa.eu/en/use-esco/download

**Version :** ESCO v1.2.1.

| Fichier | Contenu |
|---|---|
| `occupations_en.csv` | 3 043 métiers |
| `skills_en.csv` | 13 960 compétences |
| `occupationSkillRelations_data_ai_en.csv` | 674 relations filtrées |

Le fichier des relations contient un sous-ensemble
de huit métiers orientés Data, IA et développement.

Les données serviront à :

- Identifier les compétences associées aux métiers.
- Normaliser les compétences extraites des CV.
- Construire les relations dans Neo4j.
- Justifier les correspondances métiers-compétences.

### Validation du dataset

Le script `scripts/validate_esco.py` a permis de vérifier
la cohérence référentielle du sous-ensemble.

**Résultats obtenus :**

- Métiers : 3 043.
- Compétences : 13 960.
- Relations filtrées : 674.
- Relations avec métier inconnu : 0.
- Relations avec compétence inconnue : 0.

**Statut : validation référentielle réussie.**

Cette vérification ne constitue pas encore
une évaluation de la pertinence des compétences.

### 3.2 Offres d'emploi

**Source envisagée :** LinkedIn Job Postings (2023–2024),
disponible sur Kaggle.

https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

Ces données permettront d'étudier :

- Les intitulés des postes.
- Les descriptions professionnelles.
- Les compétences exigées.
- Les technologies mentionnées.

Il s'agit d'un corpus historique,
et non d'offres d'emploi nécessairement actuelles.

### 3.3 Profils étudiants

Un corpus de profils fictifs ou anonymisés
sera constitué pour les expérimentations.

Chaque profil pourra contenir :

- Formation académique.
- Projets universitaires.
- Expériences de stage.
- Compétences déclarées.
- Technologies utilisées.
- Métier cible.

---

## 4. Pipeline d'ingestion et de préparation

### 4.1 Extraction des données

Python et Pandas permettront de traiter
les fichiers CSV et JSON.

Les CV PDF seront analysés avec un outil
d'extraction de texte adapté.

Les informations extraites seront associées
à leurs documents sources.

### 4.2 Nettoyage et normalisation

Les traitements prévus comprennent :

- Suppression des doublons.
- Gestion des valeurs manquantes.
- Uniformisation des intitulés professionnels.
- Extraction des compétences.
- Normalisation des compétences avec ESCO.
- Conservation des identifiants et de la provenance.

Les correspondances incertaines seront signalées.

### 4.3 Chunking

**Stratégie envisagée :** Recursive Character Chunking.

**Taille cible :** 512 tokens.

**Overlap cible :** 64 tokens.

Métadonnées prévues :

- `doc_id`
- `chunk_id`
- `source`
- `document_type`
- `job_id`
- `profile_id`
- `esco_uri`

Les champs non applicables pourront être omis.

Les relations ESCO seront conservées
sous forme structurée et ne seront pas
découpées comme des documents textuels.

### 4.4 Génération des embeddings

**Modèle envisagé :** `BAAI/bge-m3`.

**Dimension dense :** 1 024.

Les embeddings représenteront les contenus
textuels sous forme de vecteurs numériques.

Ces vecteurs seront indexés dans Qdrant
avec les métadonnées correspondantes.

---

## 5. Recherche hybride et reranking

### 5.1 Recherche lexicale — BM25

BM25 permet de retrouver les documents
contenant les termes recherchés.

Cette approche est particulièrement utile
pour les noms de technologies et les compétences
explicitement mentionnées.

### 5.2 Recherche sémantique

La recherche sémantique utilise les embeddings
pour retrouver les contenus proches en signification,
même lorsque les mots utilisés diffèrent.

### 5.3 Fusion des résultats

Les résultats lexicaux et sémantiques
seront combinés pour améliorer le classement.

Une stratégie telle que Reciprocal Rank Fusion
(RRF) pourra être expérimentée.

### 5.4 Reranking

**Modèle envisagé :** `BAAI/bge-reranker-v2-m3`.

Le Cross-Encoder permettra de réévaluer
les passages candidats en fonction de la requête.

**Configuration cible :**

- Récupération initiale : Top-20.
- Reranking : Cross-Encoder.
- Sélection finale : Top-5.

Le reranking sera effectué dans le pipeline
applicatif après la récupération des candidats.

---

## 6. Graphe de connaissances Neo4j

Neo4j permettra de représenter les relations
entre les étudiants, les projets, les compétences
et les exigences des métiers.

### 6.1 Entités principales

| Entité | Description |
|---|---|
| Etudiant | Profil de l'utilisateur |
| Projet | Projet académique ou personnel |
| Competence | Compétence identifiée ou normalisée |
| Metier | Profession issue d'ESCO |
| OffreEmploi | Offre professionnelle étudiée |

### 6.2 Relations du graphe

| Source | Relation | Destination |
|---|---|---|
| Etudiant | REALISE | Projet |
| Projet | DOCUMENTE | Competence |
| Metier | REQUIERT | Competence |
| OffreEmploi | MENTIONNE | Competence |
| Etudiant | CIBLE | Metier |

Chaque relation conservera sa provenance
lorsque des informations justificatives existent.

### 6.3 Exemple d'exploitation

Un étudiant a réalisé un projet NLP utilisant Python.

Le graphe peut représenter :

**Projet NLP → DOCUMENTE → Python**

Pour un métier ciblé :

**GenAI Engineer → REQUIERT → Python**

Ces relations permettent de retrouver
les preuves associées à une compétence.

Elles ne suffisent pas à elles seules
à certifier la maîtrise de cette compétence
ou l'adéquation complète au métier.

---

## 7. Analyse des écarts et génération

### 7.1 Analyse des compétences

PathForge distinguera :

1. Les compétences déclarées par l'étudiant.
2. Les compétences documentées par ses expériences.
3. Les compétences exigées par le métier cible.
4. Les compétences dont les preuves sont insuffisantes.

### 7.2 Identification des écarts

Le système comparera les compétences documentées
aux exigences du métier cible.

Il identifiera les compétences exigées
mais non encore documentées dans le profil.

L'absence de preuve ne sera pas considérée
automatiquement comme une absence de maîtrise.

### 7.3 Construction du contexte GraphRAG

Le contexte de génération réunira :

- Les passages pertinents issus de Qdrant.
- Les relations pertinentes du graphe Neo4j.
- Les informations autorisées du profil étudiant.
- Les exigences du métier cible.
- Les références aux documents utilisés.

### 7.4 Recommandations personnalisées

Le LLM produira :

- Une synthèse des compétences documentées.
- Une analyse des exigences professionnelles.
- Une identification des écarts.
- Des recommandations de progression.
- Des explications accompagnées de sources.

En cas d'informations insuffisantes,
le système devra le signaler explicitement.

---

## 8. Backend et frontend

### 8.1 Backend — FastAPI

FastAPI assurera :

- La validation des requêtes avec Pydantic v2.
- L'importation des documents.
- L'orchestration du moteur GraphRAG.
- La recherche dans Qdrant.
- L'exploration des relations Neo4j.
- L'analyse des écarts.
- L'appel au LLM.
- La restitution des recommandations sourcées.

Un endpoint de streaming SSE est prévu
pour la génération progressive des réponses.

### 8.2 Frontend — React

L'application web permettra à l'étudiant de :

1. Importer son CV.
2. Renseigner ses projets et expériences.
3. Sélectionner son métier cible.
4. Visualiser les compétences documentées.
5. Consulter les compétences exigées.
6. Identifier les écarts.
7. Consulter les recommandations et leurs sources.

### 8.3 PostgreSQL

PostgreSQL sera utilisé pour stocker :

- Les profils étudiants autorisés.
- Les paramètres utilisateur.
- Le métier cible sélectionné.
- Les historiques d'analyses.
- Les références aux documents.

---

## 9. Évaluation et performances

### 9.1 Métriques principales

| Métrique | Objectif cible |
|---|---|
| Recall@10 | >= 85 % |
| Recall@5 | >= 80 % |
| Faithfulness (Ragas) | >= 0,85 |
| Answer Relevance | >= 0,80 |
| Time-to-First-Token | < 800 ms |
| Latence E2E P95 | < 3,5 s |

### 9.2 Métriques spécifiques à PathForge

- Précision d'extraction des compétences.
- Rappel d'extraction des compétences.
- Exactitude de normalisation ESCO.
- NDCG@10 pour le classement des offres.
- Cohérence des relations du graphe.
- Traçabilité des recommandations.

### 9.3 Protocole d'évaluation envisagé

Les expérimentations compareront :

1. La recherche lexicale seule.
2. La recherche sémantique seule.
3. La recherche hybride avec reranking.
4. La recherche hybride enrichie par Neo4j.

Les tests seront réalisés sur un jeu
de données et de requêtes annotées.

Les objectifs présentés sont prévisionnels
et ne constituent pas des résultats obtenus.

---

## 10. Sécurité et garde-fous

### 10.1 Protection des données personnelles

Le dépôt public utilisera des profils fictifs
ou des données anonymisées et autorisées.

Les CV réels nécessiteront un traitement
adapté, avec contrôle d'accès et conservation limitée.

### 10.2 Protection des secrets

- Aucune clé API dans le dépôt GitHub.
- Variables d'environnement pour les secrets.
- Exclusion des fichiers `.env` sensibles de Git.
- Protection des accès aux services.

### 10.3 Fiabilité des recommandations

- Conservation des références documentaires.
- Distinction entre compétences déclarées et documentées.
- Signalement des correspondances incertaines.
- Absence de conclusions sans preuves suffisantes.
- Aucune garantie automatique d'employabilité.

### 10.4 Sécurité du pipeline GraphRAG

Les documents récupérés seront considérés
comme des données non fiables.

Le système ne devra pas suivre les instructions
contenues dans un document récupéré comme
s'il s'agissait d'instructions système.

### 10.5 Isolation réseau

Qdrant, Neo4j et PostgreSQL seront configurés
dans des réseaux Docker internes
lors du déploiement complet.

Les ports seront exposés uniquement
lorsqu'ils seront nécessaires.

---

## 11. Déploiement et environnement

### 11.1 Docker Compose

Docker Compose permettra de lancer
progressivement les services nécessaires.

**Environnement déjà validé :**

- Qdrant v1.15.5 installé et démarré.
- Conteneur local fonctionnel.
- Tableau de bord Qdrant accessible.
- Fichier `docker-compose.yml` disponible sur GitHub.

L'intégration des autres services
sera réalisée progressivement.

### 11.2 CI/CD

GitHub Actions permettra :

- L'exécution des tests Pytest.
- Le linting avec Ruff.
- Les vérifications automatiques du code.
- La détection des régressions.
- Les contrôles avant fusion sur `main`.

---

## 12. État d'avancement

### Réalisé

- [x] Dépôt GitHub créé et structuré.
- [x] Référentiel ESCO v1.2.1 téléchargé.
- [x] Relations ESCO filtrées pour les métiers Data/IA.
- [x] Validation des 674 relations ESCO.
- [x] Script de validation ajouté à GitHub.
- [x] Choix de Qdrant documenté.
- [x] Docker Compose configuré.
- [x] Qdrant démarré localement.

### À réaliser

- [ ] Préparation du corpus d'offres d'emploi.
- [ ] Constitution des profils étudiants fictifs.
- [ ] Implémentation complète de l'ingestion.
- [ ] Génération et indexation des embeddings.
- [ ] Recherche hybride et reranking.
- [ ] Construction du graphe Neo4j.
- [ ] Développement du backend FastAPI.
- [ ] Développement du frontend React.
- [ ] Intégration du LLM.
- [ ] Évaluation avec Ragas.
- [ ] Tests automatisés et CI/CD.
- [ ] Déploiement final multi-services.

---

## 13. Conclusion

L'architecture de PathForge AI combine
la recherche documentaire hybride,
un graphe de connaissances
et la génération augmentée par LLM.

Cette approche permettra de relier
les expériences et compétences des étudiants
aux exigences des métiers, afin de produire
des recommandations personnalisées,
explicables et appuyées par des sources.

PathForge AI constitue un outil d'aide
à l'orientation professionnelle,
et non un système de certification automatique
des compétences ou de recrutement.
