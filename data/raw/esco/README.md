# Dataset ESCO — PathForge AI

## 1. Présentation du dataset

ESCO (*European Skills, Competences, Qualifications and Occupations*) est une classification européenne des métiers et des compétences.

Dans **PathForge AI**, ESCO constitue le référentiel de référence permettant d'identifier, de normaliser et de relier les compétences aux métiers professionnels.

Il représente une source centrale pour la recherche documentaire et pour la construction du futur graphe de connaissances.

### Informations générales

| Caractéristique | Valeur |
|---|---|
| Source | Commission européenne — ESCO |
| Version | v1.2.1 |
| Langue | Anglais |
| Format retenu | JSON |
| Nature des données | Structurées, relationnelles et textuelles |
| Couverture | Référentiel ESCO v1.2.1 en anglais, avec fichiers complémentaires sélectionnés |

**Source officielle :** https://esco.ec.europa.eu/en/use-esco/download

Les fichiers JSON sont obtenus par conversion des CSV officiels, en conservant les colonnes et les identifiants ESCO.

Le traitement local du dataset a débuté avant l'ajout de l'ensemble des fichiers sélectionnés sur GitHub.

---

## 2. Composition du dataset

Le dossier `data/raw/esco/` comprend désormais **huit fichiers JSON**.

### 2.1 Fichiers fondamentaux

| Fichier | Description | Nombre d'enregistrements |
|---|---|---:|
| `occupations.json` | Référentiel des métiers | 3 043 |
| `skills.json` | Référentiel des compétences | 13 960 |
| `occupation_skill_relations.json` | Relations métiers-compétences | 126 051 |

### 2.2 Fichiers complémentaires

| Fichier | Description | Nombre d'enregistrements |
|---|---|---:|
| `skill_skill_relations.json` | Relations entre compétences | 5 818 |
| `occupation_hierarchy.json` | Relations hiérarchiques du pilier des métiers | 3 648 |
| `skill_hierarchy.json` | Relations hiérarchiques du pilier des compétences | 20 819 |
| `isco_groups.json` | Groupes de classification professionnelle ISCO | 619 |
| `digital_skills.json` | Collection de compétences numériques | 1 284 |

Les nombres correspondent aux enregistrements contenus dans les fichiers. Ils ne représentent pas nécessairement des métiers ou compétences uniques.

### 2.3 Métiers — `occupations.json`

Ce fichier contient les informations relatives aux métiers référencés par ESCO.

Champs principaux :

- `conceptUri` : identifiant unique du métier.
- `preferredLabel` : intitulé officiel du métier.
- `description` : description du métier.
- `altLabels` : appellations alternatives.
- `iscoGroup` : groupe de classification professionnelle.

### 2.4 Compétences — `skills.json`

Ce fichier décrit les compétences et connaissances référencées dans ESCO.

Champs principaux :

- `conceptUri` : identifiant unique de la compétence.
- `preferredLabel` : intitulé de la compétence.
- `description` : description textuelle.
- `skillType` : type de compétence.
- `reuseLevel` : niveau de réutilisabilité.

### 2.5 Relations métiers-compétences — `occupation_skill_relations.json`

Ce fichier représente les relations entre métiers et compétences.

Champs principaux :

- `occupationUri` : identifiant du métier.
- `skillUri` : identifiant de la compétence.
- `relationType` : type de relation.
- `skillType` : type de compétence.

Ces relations permettent d'associer les compétences aux métiers et serviront à structurer le graphe de connaissances Neo4j.

### 2.6 Relations entre compétences — `skill_skill_relations.json`

Ce fichier contient **5 818 relations entre compétences**.

Il permettra d'enrichir le graphe de connaissances en représentant des relations supplémentaires entre les compétences du référentiel ESCO.

### 2.7 Hiérarchie des métiers — `occupation_hierarchy.json`

Ce fichier contient **3 648 relations hiérarchiques** du pilier des métiers ESCO.

Il permettra de naviguer entre les métiers et leurs catégories professionnelles en respectant les relations officielles.

### 2.8 Hiérarchie des compétences — `skill_hierarchy.json`

Ce fichier contient **20 819 relations hiérarchiques** du pilier des compétences ESCO.

Il permettra d'explorer l'organisation des compétences et leurs relations hiérarchiques.

### 2.9 Classification professionnelle — `isco_groups.json`

Ce fichier contient **619 enregistrements** relatifs à la classification professionnelle ISCO.

Il sera utile pour organiser et regrouper les métiers selon leurs catégories professionnelles.

### 2.10 Compétences numériques — `digital_skills.json`

Ce fichier contient **1 284 enregistrements** de la collection des compétences numériques ESCO.

Il présente un intérêt particulier pour les métiers Data, IA et Big Data étudiés dans PathForge AI.

---

## 3. Validation du dataset

### 3.1 Validation des fichiers fondamentaux

Les données ont été contrôlées à l'aide du script :

`scripts/validate_esco.py`

Ce script vérifie que les identifiants de métiers et de compétences utilisés dans les relations existent dans les référentiels correspondants.

### Résultats obtenus

| Vérification | Résultat |
|---|---:|
| Métiers du référentiel initial | 3 043 |
| Compétences | 13 960 |
| Relations métiers-compétences | 126 051 |
| Relations avec métier inconnu | 0 |
| Relations avec compétence inconnue | 0 |

**Statut : validation référentielle réussie.**

Commande :

`python scripts/validate_esco.py`

### 3.2 Validation des fichiers complémentaires

Les cinq fichiers complémentaires ont été convertis avec :

`scripts/convert_esco_extra.py`

Résultats de conversion :

| Fichier | Enregistrements |
|---|---:|
| `skill_skill_relations.json` | 5 818 |
| `occupation_hierarchy.json` | 3 648 |
| `skill_hierarchy.json` | 20 819 |
| `isco_groups.json` | 619 |
| `digital_skills.json` | 1 284 |

**Statut : conversion et vérification de lisibilité JSON réussies.**

Les relations supplémentaires devront faire l'objet de contrôles référentiels spécifiques avant leur exploitation complète dans Neo4j.

Cette validation ne constitue pas une évaluation exhaustive de la qualité sémantique du référentiel.

---

## 4. Utilisation des données

Le référentiel ESCO intervient dans deux traitements complémentaires de PathForge AI.

### 4.1 Recherche vectorielle — Qdrant

Lors de la séance 2, nous avons exploité localement les données ESCO pour préparer un corpus documentaire enrichi et mettre en place une recherche sémantique.

Les informations utiles ont été préparées et organisées en documents textuels, puis transformées en embeddings.

Le traitement a suivi les étapes suivantes :

1. Exploration et préparation des données ESCO.
2. Nettoyage des doublons documentaires.
3. Construction des documents métiers enrichis.
4. Découpage en chunks de 512 tokens avec overlap de 64.
5. Génération d'embeddings avec BGE-M3.
6. Indexation dans Qdrant.
7. Recherche sémantique Top-5 avec filtres et métadonnées.

### Configuration de l'indexation

| Paramètre | Valeur |
|---|---|
| Collection Qdrant | `pathforge_esco` |
| Modèle d'embeddings | `BAAI/bge-m3` |
| Dimensions | 1 024 |
| Distance | Cosine |
| Taille des chunks | 512 tokens |
| Overlap | 64 tokens |
| Métiers uniques après nettoyage | 3 039 |
| Vecteurs indexés | 3 314 |
| Chunks manquants selon le contrôle | 0 |

Les métadonnées associées aux documents comprennent notamment :

- Le métier.
- L'URI ESCO.
- La source.
- Le type de document.
- Le contenu textuel.
- Les compétences associées.

**Précision :** l'exploitation des fichiers ESCO pendant la préparation ne signifie pas que chaque ligne de chaque fichier a été indexée comme un vecteur indépendant.

Les données relationnelles peuvent contribuer à enrichir les documents sans être vectorisées individuellement.

L'ajout progressif des fichiers JSON sur GitHub correspond à la publication et à la documentation des sources. Il ne constitue pas une nouvelle indexation dans Qdrant.

### 4.2 Graphe de connaissances — Neo4j

Les relations officielles ESCO seront utilisées pour construire un graphe de connaissances.

Les principales entités envisagées sont :

- Métier.
- Compétence.
- Groupe professionnel.
- Groupe de compétences.

Les relations permettront notamment de représenter :

- Les compétences requises pour un métier.
- Les relations hiérarchiques entre métiers et classifications.
- Les relations hiérarchiques entre compétences.
- Les relations officielles entre différentes compétences.

Les identifiants ESCO permettront d'assurer la correspondance entre les données structurées de Neo4j et les documents récupérés dans Qdrant.

**État actuel :** les fichiers nécessaires sont disponibles au format JSON ; la modélisation et l'importation du graphe restent à réaliser.

---

## 5. Caractéristiques du corpus textuel

Les fichiers `occupations.json` et `skills.json` possèdent des descriptions textuelles en anglais.

Une analyse préliminaire des CSV sources a donné :

| Caractéristique | Métiers | Compétences |
|---|---:|---:|
| Nombre de documents du référentiel brut | 3 043 | 13 960 |
| Descriptions non vides | 3 043 | 13 960 |
| Longueur moyenne | 42,6 mots | 22 mots |
| Longueur maximale | 165 mots | 104 mots |

Les descriptions officielles sont relativement courtes.

Cependant, les documents métiers enrichis avec leurs compétences associées peuvent être plus longs.

C'est pourquoi nous avons utilisé une stratégie de découpage par tokens avec :

- **Chunk size :** 512 tokens.
- **Overlap :** 64 tokens.
- **Tokenizer :** celui utilisé avec BGE-M3.

Cette approche conserve un chevauchement entre les chunks afin de limiter la perte de contexte.

Le découpage utilisé est fondé sur les tokens ; il ne correspond pas à un algorithme de chunking sémantique fondé sur la détection des changements de sujet.

---

## 6. Recherche sémantique et résultats

Nous avons développé :

`scripts/search_test.py`

Ce script permet d'effectuer une recherche Top-5 dans la collection Qdrant avec un filtre sur le type de document.

### Exemple de question

**Which occupations require Python, SQL and data analysis skills?**

### Résultats obtenus

| Rang | Métier | Score |
|---|---|---:|
| 1 | Data analyst | 0,6368 |
| 2 | Database developer | 0,6179 |
| 3 | Database integrator | 0,6132 |
| 4 | Database designer | 0,6121 |
| 5 | Database administrator | 0,6023 |

Chaque résultat est accompagné de métadonnées permettant d'identifier le métier, sa source et son URI ESCO.

Les scores correspondent à des scores de similarité vectorielle, et non à des pourcentages de correspondance entre un étudiant et un métier.

Commande d'exécution :

`python scripts/search_test.py --query "Which occupations require Python, SQL and data analysis skills?"`

Ces résultats confirment le fonctionnement du premier moteur de recherche sémantique de PathForge AI.

---

## 7. Reproductibilité

Les fichiers JSON sont obtenus à partir des CSV officiels ESCO v1.2.1.

### Scripts de conversion et validation

| Script | Rôle |
|---|---|
| `scripts/convert_esco.py` | Conversion des trois fichiers fondamentaux |
| `scripts/convert_esco_extra.py` | Conversion des cinq fichiers complémentaires |
| `scripts/validate_esco.py` | Validation référentielle des données fondamentales |

### Scripts de préparation et ingestion

| Script | Rôle |
|---|---|
| `scripts/explore_esco.py` | Exploration des données |
| `scripts/prepare_esco.py` | Préparation du corpus documentaire |
| `scripts/count_chunks.py` | Comptage des chunks |
| `scripts/clean_esco.py` | Nettoyage des doublons |
| `scripts/ingest.py` | Première ingestion |
| `scripts/ingest_full.py` | Ingestion complète |
| `scripts/search_test.py` | Recherche sémantique Top-5 |

Les fichiers CSV originaux peuvent être téléchargés depuis le portail officiel ESCO.

Les fichiers temporaires utilisés localement ne sont pas nécessaires dans le dépôt GitHub.

---

## 8. État d'avancement

### Réalisé

- [x] Téléchargement d'ESCO v1.2.1.
- [x] Conversion des trois fichiers fondamentaux en JSON.
- [x] Validation des 126 051 relations métiers-compétences.
- [x] Conversion des cinq fichiers complémentaires en JSON.
- [x] Vérification de la lisibilité des huit fichiers JSON.
- [x] Préparation du corpus ESCO pour la recherche.
- [x] Nettoyage des doublons documentaires.
- [x] Découpage en chunks de 512 tokens avec overlap de 64.
- [x] Génération des embeddings avec BGE-M3.
- [x] Création de la collection `pathforge_esco`.
- [x] Indexation de 3 314 vecteurs dans Qdrant.
- [x] Vérification de l'absence de chunks manquants.
- [x] Recherche sémantique Top-5 avec métadonnées.

### À réaliser

- [ ] Validation approfondie des relations supplémentaires.
- [ ] Benchmark de deux tailles de chunks sur dix questions.
- [ ] Consolidation du script d'ingestion complet.
- [ ] Documentation des adaptations techniques de la séance 2.
- [ ] Implémentation de BM25.
- [ ] Fusion des recherches avec RRF.
- [ ] Reranking Cross-Encoder.
- [ ] Évaluation quantitative du retrieval.
- [ ] Construction du graphe Neo4j.
- [ ] Intégration des datasets LinkedIn et profils étudiants.

---

## 9. Limites du dataset

- Le référentiel exploité est en anglais.
- Les descriptions officielles sont relativement courtes.
- ESCO représente des métiers et des compétences, mais pas des offres d'emploi actualisées.
- Les informations ESCO ne suffisent pas à mesurer les compétences réelles d'un étudiant.
- Les hiérarchies et relations supplémentaires nécessitent une interprétation conforme au modèle ESCO.
- L'indexation vectorielle ne remplace pas la représentation structurée des relations.
- Les performances du moteur devront être évaluées sur des questions annotées.
- L'analyse personnalisée nécessite les profils étudiants et les offres d'emploi.

PathForge AI combine progressivement trois sources de données :

1. **ESCO :** métiers, compétences et relations.
2. **LinkedIn Job Postings :** exigences professionnelles du marché.
3. **Student Profiles :** compétences, expériences et projets des étudiants.

---

## 10. Conclusion

Le dataset ESCO v1.2.1 constitue le socle de connaissances professionnelles de PathForge AI.

Il est désormais organisé autour de **huit fichiers JSON**, contenant les métiers, les compétences, les relations et les classifications complémentaires.

Lors de la séance 2, nous avons exploité ce référentiel pour construire un premier moteur de recherche sémantique fonctionnel, avec **3 314 vecteurs indexés dans Qdrant** à l'aide de BGE-M3.

Les prochaines étapes porteront sur l'amélioration de la recherche avec BM25, RRF et Cross-Encoder, puis sur l'exploitation des relations structurées dans Neo4j.

L'objectif final est de construire un système d'orientation professionnelle capable d'analyser les profils étudiants, de les rapprocher des exigences des métiers et de générer des recommandations personnalisées, explicables et fondées sur des sources vérifiables.
