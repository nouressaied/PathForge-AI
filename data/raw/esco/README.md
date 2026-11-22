
# Dataset ESCO — PathForge AI

## 1. Présentation du dataset

ESCO (European Skills, Competences, Qualifications and Occupations)
est une classification européenne des métiers et des compétences.

Dans PathForge AI, ESCO constitue le référentiel de référence
pour identifier, normaliser et relier les compétences
aux métiers professionnels.

### Informations générales

| Caractéristique | Valeur |
|---|---|
| Source | Commission européenne — ESCO |
| Version | v1.2.1 |
| Langue | Anglais |
| Format retenu | JSON |
| Nature des données | Structurées et textuelles |
| Couverture | Référentiel ESCO complet en anglais |

**Source officielle :**
https://esco.ec.europa.eu/en/use-esco/download

Les fichiers JSON sont obtenus par conversion
des fichiers CSV officiels, sans modification
des identifiants ESCO.

## 2. Composition du dataset

Le corpus comprend trois fichiers :

| Fichier | Description | Nombre d'éléments |
|---|---|---:|
| `occupations.json` | Référentiel des métiers | 3 043 |
| `skills.json` | Référentiel des compétences | 13 960 |
| `occupation_skill_relations.json` | Relations métiers-compétences | 126 051 |

### 2.1 Métiers — occupations.json

Ce fichier contient les informations relatives
aux métiers référencés par ESCO.

Champs principaux :

- `conceptUri` : identifiant unique du métier.
- `preferredLabel` : intitulé officiel du métier.
- `description` : description du métier.
- `altLabels` : appellations alternatives.
- `iscoGroup` : groupe de classification professionnelle.

### 2.2 Compétences — skills.json

Ce fichier décrit les compétences et connaissances
référencées dans ESCO.

Champs principaux :

- `conceptUri` : identifiant unique de la compétence.
- `preferredLabel` : intitulé de la compétence.
- `description` : description textuelle.
- `skillType` : type de compétence.
- `reuseLevel` : niveau de réutilisabilité.

### 2.3 Relations — occupation_skill_relations.json

Ce fichier représente les relations entre métiers
et compétences.

Champs principaux :

- `occupationUri` : identifiant du métier.
- `skillUri` : identifiant de la compétence.
- `relationType` : type de relation.
- `skillType` : type de compétence.

Ces relations serviront à construire
le graphe de connaissances Neo4j.

Elles ne seront pas découpées artificiellement
en chunks pour la recherche vectorielle.

## 3. Validation du dataset

Les données ont été contrôlées à l'aide du script :

`scripts/validate_esco.py`

Ce script vérifie que chaque identifiant de métier
et de compétence présent dans les relations
existe dans les référentiels correspondants.

### Résultats obtenus

| Vérification | Résultat |
|---|---:|
| Métiers | 3 043 |
| Compétences | 13 960 |
| Relations | 126 051 |
| Relations avec métier inconnu | 0 |
| Relations avec compétence inconnue | 0 |

**Statut : validation référentielle réussie.**

Commande d'exécution depuis la racine du projet :

    python scripts/validate_esco.py

Cette validation confirme la cohérence des identifiants.
Elle ne constitue pas une validation exhaustive
de la qualité sémantique du référentiel.

## 4. Utilisation des données

Le dataset ESCO intervient dans deux traitements
complémentaires de PathForge AI.

### 4.1 Recherche vectorielle — Qdrant

Les intitulés et descriptions des métiers
et des compétences seront transformés
en documents textuels.

Ces documents seront ensuite :

1. Nettoyés et préparés.
2. Découpés si nécessaire.
3. Transformés en embeddings.
4. Indexés dans Qdrant avec leurs métadonnées.

Les métadonnées permettront de conserver
la provenance et les identifiants ESCO.

### 4.2 Graphe de connaissances — Neo4j

Les relations officielles entre métiers et compétences
seront utilisées pour construire le graphe.

Les identifiants ESCO permettront d'assurer
la correspondance entre les entités du graphe
et les documents retrouvés dans Qdrant.

## 5. Caractéristiques du corpus textuel

Les deux fichiers `occupations.json` et `skills.json`
possèdent des descriptions textuelles en anglais.

Une analyse préliminaire des CSV sources a donné :

| Caractéristique | Métiers | Compétences |
|---|---:|---:|
| Nombre de documents | 3 043 | 13 960 |
| Descriptions non vides | 3 043 | 13 960 |
| Longueur moyenne | 42,6 mots | 22 mots |
| Longueur maximale | 165 mots | 104 mots |

Les descriptions étant relativement courtes,
la stratégie d'ingestion privilégiera
la conservation d'une fiche entière
lorsqu'elle respecte la taille maximale choisie.

Un découpage sera appliqué uniquement
aux documents dépassant cette limite.

## 6. Reproductibilité

La conversion depuis les fichiers CSV officiels
est réalisée par :

`scripts/convert_esco.py`

La validation des fichiers JSON est réalisée par :

`scripts/validate_esco.py`

Les CSV sources sont téléchargeables
depuis le portail officiel ESCO.

Le script de conversion nécessite
les fichiers CSV sources pour être réexécuté.

## 7. État de préparation

### Réalisé

- [x] Téléchargement du référentiel ESCO v1.2.1.
- [x] Conversion des métiers au format JSON.
- [x] Conversion des compétences au format JSON.
- [x] Conversion des relations complètes au format JSON.
- [x] Vérification des 126 051 relations.
- [x] Validation des identifiants métiers et compétences.

### À réaliser

- [ ] Préparation des documents pour l'ingestion.
- [ ] Implémentation du chunking.
- [ ] Génération des embeddings.
- [ ] Indexation des documents dans Qdrant.
- [ ] Recherche sémantique Top-5.
- [ ] Construction du graphe Neo4j.

## 8. Limites du dataset

- Le référentiel exploité est en anglais.
- Les descriptions sont souvent courtes.
- ESCO est un référentiel de métiers et de compétences,
  et non un corpus d'offres d'emploi actuelles.
- Les données ESCO ne permettent pas, seules,
  d'évaluer les compétences réelles d'un étudiant.
- Des profils étudiants et des offres d'emploi
  seront nécessaires pour les fonctionnalités
  complètes de PathForge AI.
