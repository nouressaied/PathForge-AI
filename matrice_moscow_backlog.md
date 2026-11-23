# Backlog Technique MoSCoW — Projet Fédérateur AI-BD_BI
## Découpage Agile des User Stories & Critères d'Acceptation

---

## 1. MUST HAVE (Indispensables pour la Livraison Finale S7)

*Ce sont les fonctionnalités non négociables qui conditionnent la validation du diplôme d'ingénieur.*

| ID | User Story Technique | Critères d'Acceptation (DoD) | Séance Cible |
| :-: | :--- | :--- | :-: |
| **US-01** | **Ingestion & Chunking Structuré**<br>En tant que Data Engineer, je veux découper le corpus en chunks avec métadonnées pour permettre un indexage précis. | - Script Python asynchrone avec gestion des erreurs.<br>- Métadonnées stockées : `doc_id`, `page_number`, `chunk_id`, `source`.<br>- Pas de perte d'information sur les tableaux. | **S2** |
| **US-02** | **Indexation Vectorielle HNSW**<br>En tant que système RAG, je veux insérer les vecteurs denses dans la base vectorielle pour accélérer la recherche sémantique. | - Base vectorielle démarrée via Docker Compose.<br>- Index HNSW configuré avec distance Cosine.<br>- Temps d'insertion $< 50$ ms par batch de 64 chunks. | **S2** |
| **US-03** | **Retrieval Hybride & Reranking**<br>En tant que moteur de recherche, je veux fusionner les scores denses et BM25 puis reranker pour maximiser la pertinence. | - Top-20 initial généré en recherche hybride.<br>- Modèle Cross-Encoder réduisant la liste au Top-5.<br>- Métrique Recall@5 mesurée $\ge 80\%$. | **S3** |
| **US-04** | **API REST FastAPI & Schémas Pydantic v2**<br>En tant qu'application cliente, je veux interroger l'API via des endpoints typés et validés. | - Schémas `QueryRequest` et `QueryResponse` Pydantic v2 stricts.<br>- Rejet immédiat en code HTTP 422 si chaîne vide ou hors limites.<br>- Documentation OpenAPI / Swagger interactive générée. | **S4** |
| **US-05** | **Génération de Réponse en Streaming SSE**<br>En tant qu'utilisateur, je veux recevoir la réponse mot par mot avec les citations des chunks pour réduire la latence perçue. | - Endpoint `/api/v1/chat/stream` émettant des Server-Sent Events.<br>- Payload SSE transmettant les chunks sources et les scores de similarité.<br>- Time-to-First-Token $< 800$ ms. | **S4 / S5** |
| **US-06** | **Interface Web Réactive (React / Angular)**<br>En tant qu'utilisateur final, je veux saisir ma question et visualiser la réponse en streaming ainsi que les sources citées. | - Composant chat moderne avec gestion des états (idle, loading, error).<br>- Tiroir ou carte latérale inspectant le texte exact des chunks cités.<br>- Zéro rechargement de page. | **S5** |
| **US-07** | **Assurance Qualité & CI/CD Automatisée**<br>En tant que Lead Developer, je veux que chaque commit déclenche des tests avec mocks et le linter Ruff. | - 4 tests Pytest obligatoires (mock LLM et VectorDB sans coût).<br>- Workflow GitHub Actions vert bloquant tout merge non conforme. | **S6** |
| **US-08** | **Conteneurisation de Production Multi-Stage**<br>En tant qu'ingénieur DevOps, je veux déployer le système complet via Docker Compose de production sécurisé. | - Dockerfile multi-stage avec utilisateur non-root.<br>- Secrets injectés uniquement par variables d'environnement. | **S7** |

---

## 2. SHOULD HAVE (Forte Valeur Ajoutée Industrielle)

*Fonctionnalités renforçant la robustesse et la maturité MLOps de la solution.*

| ID | User Story Technique | Critères d'Acceptation | Séance Cible |
| :-: | :--- | :--- | :-: |
| **US-09** | **Tracing MLOps Distribué (Langfuse / OpenTelemetry)**<br>En tant que responsable IA, je veux tracer chaque étape de la chaîne RAG pour identifier les goulets d'étranglement. | - Latence découpée par étape (Embedding, Vector Search, Rerank, LLM).<br>- Nombre de tokens consommés et coût estimé enregistrés. | **S3 / S4** |
| **US-10** | **Cache Sémantique Redis**<br>En tant qu'architecte système, je veux cacher les requêtes similaires pour économiser les coûts d'appel LLM. | - Seuil de similarité cosinus $> 0.95$ pour servir le cache en $< 50$ ms.<br>- Invalidation configurable du cache. | **S4** |
| **US-11** | **Évaluation Continue Ragas**<br>En tant que Data Scientist, je veux évaluer automatiquement les réponses sur un benchmark de référence. | - Pipeline d'évaluation périodique calculant Faithfulness et Answer Relevance. | **S3** |

---

## 3. COULD HAVE (Différenciateurs M2 Optionnels)

*Fonctionnalités avancées pour les équipes visant l'excellence d'ingénierie.*

| ID | User Story Technique | Critères d'Acceptation |
| :-: | :--- | :--- |
| **US-12** | **Manifestes Kubernetes de Déploiement** | Déploiement K8s complet (Deployments, Services, ConfigMaps, Ingress et HPA). |
| **US-13** | **Routage Agentique Multi-Outils (Query Routing)** | Dispatch automatique entre retrieval documentaire, requête SQL décisionnelle et calculatrice. |
| **US-14** | **Support Multimodal (Image + Tableau)** | Ingestion et vectorisation de tableaux complexes et schémas via modèle de vision. |

---

## 4. WON'T HAVE (Exclus du Périmètre Projet)

*Ces éléments sont explicitement exclus pour éviter la dispersion :*
- Entraînement complet *from scratch* ou pré-entraînement de fondations de modèles LLM 70B.
- Facturation SaaS complète avec paiement Stripe et gestion d'abonnements complexes.
- Interface mobile native iOS / Android (l'interface web responsive suffit amplement).


---

## 5. Adaptation spécifique — PathForge AI (complément au gabarit officiel)

**Principe :** les US-01 à US-14, leur priorité et leurs critères d’acceptation ci-dessus sont conservés tels que fournis par le professeur. Les besoins spécifiques ci-dessous s’ajoutent sans les remplacer.

| ID | Priorité | User Story PathForge AI | Critère d’acceptation envisagé | Séance cible |
| :-- | :-- | :-- | :-- | :--: |
| PF-01 | MUST | En tant qu’étudiant, je veux analyser un profil fictif contenant projets et compétences. | Profil JSON validé ; compétences extraites et affichées avec provenance. | S2–S4 |
| PF-02 | MUST | En tant qu’étudiant, je veux consulter les métiers et compétences associés issus du référentiel ESCO. | Documents indexés dans Qdrant ; réponse citant des extraits sources. | S2–S5 |
| PF-03 | MUST | En tant qu’étudiant, je veux identifier les écarts entre mon profil et un métier. | Liste des compétences présentes/manquantes et preuves documentaires affichées. | S3–S5 |
| PF-04 | SHOULD | En tant qu’étudiant, je veux explorer des relations métier–compétence–formation. | Démonstration d’une traversée Neo4j multi-sauts sur un jeu contrôlé. | S3–S5 |
| PF-05 | SHOULD | En tant que responsable IA, je veux tracer les essais du pipeline. | Comparaison reproductible de configurations avec MLflow, en complément du tracing prévu par US-09. | S3–S6 |
| PF-06 | COULD | En tant que conseiller carrière, je veux exporter un plan de progression. | Export PDF contenant recommandations et références. | Après MVP |
| PF-07 | WON'T | En tant qu’utilisateur, je veux candidater automatiquement. | Fonction explicitement exclue de la V1. | — |

**Point de vigilance :** la consigne S1 mentionne Kubernetes en « Could Have », tandis que le programme S7 prévoit des manifests de déploiement. Nous conservons l’US-12 officielle et préparerons les manifests demandés à la séance 7.
