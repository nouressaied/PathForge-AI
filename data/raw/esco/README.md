\# ESCO Dataset — PathForge AI



\## 1. Description



ESCO (European Skills, Competences, Qualifications and Occupations)

est le référentiel européen des métiers et des compétences.



Il constitue une source de référence pour la normalisation

des compétences et la construction du graphe de connaissances

de PathForge AI.



\- \*\*Version :\*\* ESCO v1.2.1

\- \*\*Langue :\*\* anglais

\- \*\*Format retenu :\*\* JSON

\- \*\*Source :\*\* https://esco.ec.europa.eu/en/use-esco/download



\## 2. Composition du dataset



| Fichier | Contenu | Nombre |

|---|---|---:|

| `occupations.json` | Métiers ESCO | 3 043 |

| `skills.json` | Compétences ESCO | 13 960 |

| `occupation\_skill\_relations.json` | Relations métiers-compétences | 126 051 |



Les fichiers JSON sont obtenus par conversion

des fichiers CSV officiels ESCO v1.2.1.



Les identifiants d'origine sont conservés.



\## 3. Typologie des données



\### Métiers



Chaque métier possède notamment :



\- Un identifiant officiel `conceptUri`.

\- Un intitulé `preferredLabel`.

\- Une description textuelle.

\- Des informations de classification.



\### Compétences



Chaque compétence contient notamment :



\- Un identifiant officiel `conceptUri`.

\- Un intitulé `preferredLabel`.

\- Une description.

\- Des informations complémentaires.



\### Relations



Les relations sont représentées par :



\- `occupationUri`

\- `skillUri`

\- `relationType`

\- `skillType`



Ces données permettront de construire

les associations métiers-compétences dans Neo4j.



\## 4. Validation des données



Le script `scripts/validate\_esco.py`

vérifie l'intégrité référentielle des relations.



Commande :



&#x20;   python scripts/validate\_esco.py



Résultats :



\- 3 043 métiers.

\- 13 960 compétences.

\- 126 051 relations.

\- 0 métier inconnu.

\- 0 compétence inconnue.



\*\*Statut : validation référentielle réussie.\*\*



Cette validation ne mesure pas encore

la pertinence sémantique des données.



\## 5. Utilisation dans PathForge AI



\### Qdrant



Les intitulés et descriptions des métiers

et compétences seront préparés comme documents textuels,

puis transformés en embeddings pour la recherche vectorielle.



\### Neo4j



Les relations métiers-compétences seront utilisées

pour construire le graphe de connaissances.



\### GraphRAG



Les informations retrouvées permettront

de comparer les compétences documentées des étudiants

aux exigences des métiers et de générer

des recommandations sourcées.



\## 6. Pipeline de préparation



1\. Chargement des données JSON.

2\. Extraction des informations textuelles.

3\. Nettoyage et préparation des documents.

4\. Chunking adapté à la longueur des textes.

5\. Génération des embeddings.

6\. Indexation des vecteurs dans Qdrant.

7\. Recherche sémantique Top-k.



\## 7. État d'avancement



\- \[x] Téléchargement du référentiel officiel ESCO v1.2.1.

\- \[x] Conversion complète des CSV en JSON.

\- \[x] Validation des 126 051 relations.

\- \[x] Vérification des identifiants métiers et compétences.

\- \[ ] Préparation des documents pour l'ingestion.

\- \[ ] Chunking et génération des embeddings.

\- \[ ] Indexation Qdrant.

\- \[ ] Recherche sémantique Top-5.

\- \[ ] Construction du graphe Neo4j.



\## 8. Limites



Le corpus ESCO est en anglais.



Ses descriptions sont relativement courtes :

le découpage sera donc adapté à leur longueur.



Le référentiel ne représente pas directement

l'ensemble des offres d'emploi actuelles du marché.



