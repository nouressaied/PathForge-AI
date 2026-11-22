# Répartition de l'équipe — PathForge AI

## 1. Composition de l'équipe

Le projet PathForge AI est réalisé par trois membres, chacun responsable d'un module d'intelligence artificielle.

| Membre | Rôle principal | Module |
|---|---|---|
| **Essaied Nour** | Lead Career Copilot & Recommendation AI | LLM, orchestration GraphRAG, analyse des écarts et recommandations |
| **Fourati Yosr** | Lead Job & Career Intelligence AI | Analyse des offres, recherche hybride, Neo4j et Graph Retrieval |
| **Trabelsi Nidhal** | Lead Profile Intelligence AI | CV Parsing, extraction LLM, Document RAG et analyse du profil |

L'organisation vise une répartition équilibrée du travail, en permettant à chaque membre de contribuer directement au développement des composants IA, LLM et RAG.

Chaque membre est responsable de son module, depuis le traitement des données jusqu'aux API et à l'intégration dans la plateforme commune.

---

## 2. Responsabilités principales

### 2.1 Trabelsi Nidhal — Profile Intelligence AI

**Spécialité : LLM + Document RAG**

**Objectif :** comprendre le profil académique et professionnel de l'étudiant.

**Responsabilités :**

- Développement du système de parsing des CV.
- Extraction des informations des projets et stages.
- Utilisation du LLM pour extraire les compétences, expériences et formations.
- Développement du Document RAG appliqué au profil étudiant.
- Utilisation de la recherche hybride Qdrant + BM25 via le moteur de recherche commun.
- Analyse et classification des compétences du candidat.
- Normalisation des compétences avec ESCO.
- Identification des preuves associées aux compétences.
- Développement de l'API Profile Analysis.
- Développement de l'interface de consultation du profil.

**Livrable :** un module permettant d'importer un CV et de produire un profil candidat structuré, contenant les compétences, expériences, formations et preuves disponibles.

**Sortie :** `StudentProfile`

---

### 2.2 Fourati Yosr — Job & Career Intelligence AI

**Spécialité : LLM + Hybrid RAG + GraphRAG**

**Objectif :** comprendre les métiers, les offres d'emploi et les exigences professionnelles.

**Responsabilités :**

- Préparation et validation des datasets ESCO et LinkedIn Job Postings.
- Analyse des descriptions d'offres avec un LLM.
- Extraction des compétences requises pour chaque métier.
- Normalisation des compétences professionnelles avec ESCO.
- Construction du Knowledge Graph dans Neo4j.
- Développement des relations métiers-compétences-offres.
- Implémentation du Graph Retrieval avec Cypher.
- Développement du moteur commun de recherche hybride avec Qdrant et BM25.
- Recherche et récupération des offres d'emploi pertinentes.
- Analyse des relations entre métiers, compétences et exigences professionnelles.
- Développement de l'API Job & Career Intelligence.
- Évaluation de la pertinence du retrieval.

**Livrable :** un moteur intelligent capable d'identifier les métiers et les offres pertinents, leurs compétences requises et les relations qui les justifient.

**Sortie :** `JobRequirements`

---

### 2.3 Essaied Nour — Career Copilot & Recommendation AI

**Spécialité : LLM + RAG Orchestration + Recommendation**

**Objectif :** transformer les informations sur l'étudiant et le marché de l'emploi en recommandations professionnelles personnalisées.

**Responsabilités :**

- Développement du Career Assistant basé sur un LLM.
- Orchestration des modules Profile Intelligence et Job & Career Intelligence.
- Intégration du Hybrid RAG et du Graph Retrieval.
- Construction du contexte utilisé par le LLM.
- Développement du Skill Gap Analysis.
- Identification des compétences documentées et des compétences à approfondir.
- Recommandation des métiers adaptés au profil étudiant.
- Génération de Personalized Learning Roadmaps.
- Intégration du Cross-Encoder pour le reranking.
- Génération de recommandations accompagnées de sources.
- Évaluation avec Ragas et des métriques personnalisées.
- Développement de l'API Career Copilot.
- Coordination de l'intégration des réponses entre les modules.

**Livrable :** un assistant intelligent capable de suggérer des métiers, d'expliquer les écarts de compétences et de générer un parcours de progression personnalisé.

**Sortie :** `CareerRecommendation`

---

## 3. Architecture globale et collaboration

Les trois modules communiquent pour produire une orientation professionnelle personnalisée.

### Entrées utilisateur

- CV et expériences académiques.
- Projets et stages.
- Compétences déclarées.
- Objectif professionnel, lorsqu'il est renseigné.

### Module 1 — Profile Intelligence AI

**Responsable : Trabelsi Nidhal**

CV + Projets + Stages

→ Parsing et extraction LLM

→ Identification des compétences

→ Document RAG

→ Profil structuré : `StudentProfile`

### Module 2 — Job & Career Intelligence AI

**Responsable : Fourati Yosr**

ESCO + LinkedIn Job Postings

→ Analyse LLM des offres

→ Extraction des exigences

→ Recherche hybride Qdrant + BM25

→ Exploration du graphe Neo4j

→ Exigences structurées : `JobRequirements`

### Module 3 — Career Copilot & Recommendation AI

**Responsable : Essaied Nour**

`StudentProfile` + `JobRequirements`

→ Orchestration RAG et Graph Retrieval

→ Reranking

→ Comparaison des compétences

→ Skill Gap Analysis

→ Génération de recommandations avec LLM

→ `CareerRecommendation`

### Résultat final

**Personalized Career Roadmap**

La plateforme doit permettre à l'étudiant de :

1. Comprendre les compétences documentées dans son profil.
2. Découvrir des métiers potentiellement adaptés.
3. Comparer son profil aux exigences professionnelles.
4. Identifier les compétences à approfondir.
5. Obtenir un parcours de progression personnalisé.
6. Consulter les sources justifiant les recommandations.

---

## 4. Matrice des responsabilités techniques

| Composant | Trabelsi Nidhal | Fourati Yosr | Essaied Nour |
|---|---|---|---|
| Module principal | Profile Intelligence | Job & Career Intelligence | Career Copilot |
| LLM | CV Extraction | Job Analysis | Recommendations |
| RAG | Document RAG | Hybrid RAG + Graph Retrieval | RAG Orchestration |
| Base de données principale | Accès Qdrant | Qdrant + Neo4j | PostgreSQL / Intégration |
| Backend | Profile API | Job API | Copilot API |
| Évaluation | Extraction Quality | Retrieval Quality | Answer Quality |
| Interface | Profil étudiant | Recherche de métiers et offres | Chatbot et Roadmap |
| Données principales | CV, projets, stages | ESCO, LinkedIn | Résultats des modules |
| Sortie | StudentProfile | JobRequirements | CareerRecommendation |

Chaque membre développe son module de bout en bout.

La recherche hybride repose sur un moteur commun afin d'éviter la duplication des composants Qdrant, BM25 et des embeddings.

---

## 5. Responsabilités transversales

Certains composants nécessitent une collaboration entre les trois membres.

| Activité | Organisation |
|---|---|
| Architecture générale | Travail commun |
| Choix des modèles LLM | Décision commune |
| Schémas JSON et modèles Pydantic | Définition commune |
| Backend FastAPI | Chaque membre développe ses API |
| Frontend React | Chaque membre contribue à l'interface de son module |
| Intégration des modules | Coordination par Essaied Nour |
| Docker Compose et environnement | Travail commun, responsable opérationnel à confirmer |
| PostgreSQL | Intégration applicative coordonnée |
| GitHub Actions et CI/CD | Travail commun |
| Tests d'intégration | Travail commun |
| Documentation | Chaque membre documente son module |
| Soutenance | Travail commun |

Les responsabilités transversales seront précisées lors de la planification technique.

---

## 6. Planning de développement

| Période | Objectif |
|---|---|
| Semaine 1 | Architecture, environnement, choix des modèles et contrats API |
| Semaines 2–3 | Développement parallèle des trois modules LLM + RAG |
| Semaine 4 | Intégration des modules et communication entre les API |
| Semaine 5 | Tests, évaluation, optimisation et démonstration |

Ce planning est prévisionnel et devra être adapté au calendrier des séances et aux contraintes du projet.

---

## 7. Organisation GitHub

### Branches proposées

- `main` : version intégrée.
- `feature/profile-intelligence-*` : module Profile Intelligence.
- `feature/job-intelligence-*` : module Job & Career Intelligence.
- `feature/career-copilot-*` : module Career Copilot.
- `feature/integration-*` : intégration transversale.

### Workflow

1. Créer une issue pour chaque tâche.
2. Développer dans une branche dédiée.
3. Exécuter les tests du module.
4. Ouvrir une Pull Request.
5. Effectuer une revue de code croisée.
6. Fusionner après validation.

---

## 8. Règles de collaboration

Afin d'assurer la cohérence technique du projet :

1. Utiliser un modèle LLM commun au départ.
2. Définir des formats JSON partagés entre les modules.
3. Centraliser les composants de recherche communs.
4. Documenter les API et leurs contrats.
5. Organiser une intégration régulière.
6. Effectuer des revues de code croisées.
7. Partager les données, les scripts et les résultats de benchmark.
8. Ne jamais publier de données personnelles réelles ou de secrets dans le dépôt public.
9. Préserver les références aux documents sources.
10. Valider le fonctionnement global avant chaque démonstration.

---

## 9. Les trois axes de PathForge AI

| Axe | Module | Responsable |
|---|---|---|
| **Comprendre le candidat** | Profile Intelligence AI | Trabelsi Nidhal |
| **Analyser le marché** | Job & Career Intelligence AI | Fourati Yosr |
| **Recommander un parcours** | Career Copilot & Recommendation AI | Essaied Nour |

L'objectif final est de réunir trois moteurs intelligents complémentaires dans une seule plateforme.

**PathForge AI : Analyser → Comparer → Recommander → Progresser.**
