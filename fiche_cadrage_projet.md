# Fiche de Cadrage d’Ingénierie — Projet Fédérateur AI-BD_BI
## Spécification du Moteur RAG / Data Intelligent

---

### 1. Fiche d'Identité du Projet

- **Nom du Projet :** PathForge AI — Plateforme intelligente d’orientation professionnelle par RAG hybride et GraphRAG
- **Membres de l'Équipe :**
  1. [Nom Prénom — Lead Data / Retrieval]
  2. [Nom Prénom — Lead Backend / MLOps]
  3. [Nom Prénom — Lead Frontend / Infra]
- **Lien du Dépôt GitHub :** À renseigner après création du dépôt
- **Branche de travail principale :** `main` (protection à configurer)

---

### 2. Cadrage du Problème Métier ("Problem-First")

#### 2.1 Persona Cible & Contexte Opérationnel
- **Utilisateur visé :** Étudiant en dernière année d’études supérieures ou jeune diplômé souhaitant identifier des métiers adaptés à son profil. Un conseiller carrière pourra être un utilisateur secondaire à terme.
- **Point de douleur majeur (Pain point) :** Un diplôme identique peut masquer des parcours, projets, stages et compétences différents. L’étudiant peine à relier ses acquis aux compétences demandées par les métiers et à identifier un plan concret pour combler les écarts.
- **Limite des approches classiques (Pourquoi l'IA générative ?) :** Les filtres et recherches lexicales simples ne rapprochent pas systématiquement les synonymes de compétences, les descriptions libres de projets et les chaînes de relations métier → compétence → formation. Un LLM seul risque d’affirmer des correspondances non étayées. Le RAG hybride fournit des extraits documentaires, tandis que le graphe explicite les liens multi-étapes.

#### 2.2 Proposition de Valeur
PathForge AI analysera un profil étudiant (CV, projets et stages), retrouvera des preuves dans les référentiels métiers et offres, identifiera les compétences acquises et manquantes, puis proposera des métiers et parcours de progression **avec citations vérifiables**. L’interface cible affichera les réponses en streaming et permettra d’inspecter les passages sources. Il s’agit d’une aide à la décision, non d’une garantie d’embauche.

---

### 3. Données & Volumétrie

- **Format des données sources :** `[ ] PDF multi-colonnes` `[x] JSON/CSV` `[ ] Tables relationnelles SQL` `[x] Markdown` `[ ] Images/Scans` (PDF CV éventuels en extension après validation du pipeline)
- **Sources envisagées :**
  - **ESCO** (https://esco.ec.europa.eu/) : référentiel métiers, compétences et relations, à télécharger dans le format disponible.
  - **France Travail** (https://francetravail.io/) : offres d’emploi via API, **sous réserve d’accès et de conditions d’utilisation**.
  - **Profils fictifs annotés** : CV, projets et stages structurés en JSON/Markdown pour tester la personnalisation sans exposer de données personnelles réelles.
  - **France Compétences** (https://www.francecompetences.fr/) : référentiels de certifications et formations, **modalités d’accès et de réutilisation à vérifier**.
- **Volumétrie initiale (PoC S1-S3) :** Cible indicative : 100 métiers, 500 compétences, 50 offres, 20 profils fictifs, 50 formations/certifications. **Ce ne sont pas des données déjà collectées.** Le nombre réel de documents et chunks sera calculé après extraction et chunking.
- **Volumétrie cible en production :** À définir à partir de la volumétrie effectivement accessible, du nombre de chunks, de la latence et de la capacité des services. Aucune estimation non mesurée n’est présentée comme acquise.
- **Fréquence de mise à jour des données :** `[x] Batch quotidien` (offres, si accès autorisé) `[ ] Temps réel / Streaming` `[x] Statique` (version initiale du référentiel ESCO, actualisable lors des nouvelles publications).

---

### 4. Architecture Technique & Composants RAG

- **Stratégie de Chunking :** `[x] Recursive Character` `[ ] Semantic Chunking` `[ ] Parent-Document / Hierarchical`
  - **Taille de chunk visée :** 512 tokens ; **Overlap :** 64 tokens. Paramètres initiaux à tester ; conserver les frontières de fiches métiers/compétences et les identifiants ESCO.
  - **Comparaison S2 :** tester une deuxième stratégie (semantic ou segmentation structurée) sur dix questions, avec la même méthode d’évaluation.
- **Modèle d'Embeddings :** `BAAI/bge-m3` (**1024 dimensions**), multilingue. Choix initial soumis à un test de vitesse et de mémoire sur le poste Windows ; prévoir un modèle plus léger si nécessaire.
- **Base Vectorielle retenue :** `[x] Qdrant` `[ ] Milvus` `[ ] pgvector`
  - **Justification :** index HNSW, distance cosinus, filtres par métadonnées et exécution via Docker Compose. Payloads prévus : `doc_id`, `page_number` (null si non applicable), `chunk_id`, `source`, `type_document`, `metier_id`, `langue`.
- **Reranker (Cross-Encoder) :** `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` comme candidat initial, à comparer à d’autres modèles adaptés au français en S3.
- **LLM de Génération :** modèle instruct capable de répondre en français, via API ou service local à choisir selon coût, latence, confidentialité et accès ; décision à valider expérimentalement avant S4.
- **Recherche hybride prévue en S3 :** dense + BM25, fusion Reciprocal Rank Fusion (RRF), puis reranking Cross-Encoder.
- **Extension GraphRAG :** Neo4j pour relier `Métier → requiert → Compétence` et `Formation → développe → Compétence`. **Complément au socle RAG obligatoire**, non substitut à Qdrant.
- **Application cible :** React/Next.js → FastAPI async/Pydantic v2 → recherche Qdrant et Neo4j → LLM ; PostgreSQL pour les données applicatives, SSE pour le streaming, Ragas pour l’évaluation, traçage MLOps selon le backlog.

---

### 5. Métriques Quantitatives & SLAs

| Métrique | Définition / Outil | Objectif Cible (KPI) |
| :--- | :--- | :---: |
| **Recall@10 (Retrieval)** | Proportion des questions du jeu de référence pour lesquelles un document pertinent apparaît dans le top-10 | **≥ 85 %** |
| **Faithfulness (Ragas)** | Degré de fidélité des assertions de la réponse aux extraits récupérés | **≥ 0,85 / 1,00** |
| **Answer Relevance (Ragas)** | Adéquation de la réponse à la question posée | **≥ 0,80 / 1,00** |
| **Latence First-Token (TTFT)** | Temps entre l’envoi de la requête et le premier token affiché via SSE | **< 800 ms** |
| **Latence E2E P95** | 95e percentile du temps total de complétion des requêtes | **< 3,5 s** |

**Protocole envisagé :** constituer un Golden Dataset de questions, passages attendus et réponses de référence ; journaliser latences et configurations ; comparer dense seul, dense+BM25 et reranking. Les seuils sont **des objectifs imposés par le gabarit**, non des résultats mesurés. Le protocole et la taille du jeu de test seront documentés lors de S2/S3.

---

### 6. Gestion des Risques & Garde-fous

- **Prévention des Hallucinations :** directive de génération : « Si l’information n’est pas présente dans les extraits ci-dessus, répondez explicitement que le corpus ne permet pas de conclure. » Exiger des citations vérifiables ; exposer les chunks dans le Source Drawer ; évaluer avec Ragas.
- **Protection des Secrets :** stocker clés API et identifiants dans `.env` local, exclu de Git ; versionner uniquement `.env.example` sans secrets.
- **Isolation Réseau :** Qdrant et PostgreSQL dans un réseau Docker interne privé ; n’exposer que les ports nécessaires au développement local.
- **Confidentialité :** utiliser des profils fictifs pour le PoC ; ne pas ingérer de vrais CV sans base légale, consentement approprié et politique de conservation.
- **Fraîcheur et licences des données :** conserver `source`, version et date de collecte ; vérifier les droits d’accès et de réutilisation des APIs et référentiels.
- **Biais de recommandation :** présenter les suggestions comme une aide à l’orientation, afficher les compétences manquantes et permettre à l’utilisateur de corriger son profil.
- **Risques techniques :** surveiller consommation RAM, temps d’embedding et latence ; prévoir un modèle d’embedding plus léger et un corpus réduit pour le PoC.
