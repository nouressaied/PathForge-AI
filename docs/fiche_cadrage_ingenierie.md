
# Fiche de cadrage d'ingénierie — PathForge AI

## 1. Identification du projet

**Nom :** PathForge AI

**Domaine :** Intelligence artificielle, Big Data et GraphRAG.

**Nature :** Projet académique d'ingénierie.

**Équipe :**
- Essaied Nour
- Fourati Yosr
- Trabelsi Nidhal

## 2. Contexte et problématique

Les étudiants développent des compétences à travers
leurs formations, stages et projets universitaires.

Cependant, la correspondance entre leurs acquis
et les compétences exigées par les entreprises
reste souvent difficile à établir.

Les solutions de matching classiques reposent
principalement sur les mots-clés des CV.

Elles ne permettent pas toujours de distinguer :
- Une compétence simplement déclarée.
- Une compétence documentée par un projet.
- Une compétence exigée par un métier.
- Une compétence pour laquelle les preuves manquent.

### Problématique centrale

Comment concevoir un système intelligent capable
de relier les compétences documentées des étudiants
aux exigences des métiers, afin de produire
des recommandations personnalisées, explicables
et fondées sur des sources vérifiables ?

## 3. Objectifs du projet

### Objectif général

Développer une plateforme d'aide à l'orientation
professionnelle exploitant une architecture GraphRAG
hybride.

### Objectifs spécifiques

1. Exploiter des données professionnelles réelles.
2. Extraire les compétences des profils étudiants.
3. Normaliser les compétences avec ESCO.
4. Associer les compétences aux projets et métiers.
5. Implémenter une recherche documentaire hybride.
6. Identifier les écarts avec un métier cible.
7. Générer des recommandations sourcées.
8. Évaluer la pertinence et la fiabilité du système.

## 4. Utilisateurs et scénario principal

### Utilisateur cible

Étudiant souhaitant comprendre son positionnement
par rapport aux compétences d'un métier donné.

### Scénario

1. L'étudiant importe son CV.
2. Il renseigne ses projets et expériences.
3. Il sélectionne un métier cible.
4. La plateforme identifie les compétences documentées.
5. Elle compare le profil aux exigences du métier.
6. Elle affiche les écarts identifiés.
7. Elle propose des recommandations argumentées.

## 5. Données et contraintes

### Sources prévues

| Source | Nature | Utilisation |
|---|---|---|
| ESCO v1.2.1 | CSV structurés | Métiers, compétences et relations |
| Offres LinkedIn historiques | Données textuelles | Exigences professionnelles |
| Profils étudiants | PDF, JSON | Expériences et compétences |

### Volumes actuellement disponibles

- 3 043 métiers ESCO.
- 13 960 compétences ESCO.
- 674 relations filtrées pour huit métiers Data/IA.

Ces relations ont été vérifiées par un script Python.

Les autres corpus restent à constituer.

### Contraintes

- Données hétérogènes.
- Ambiguïté des noms de compétences.
- Difficulté de normalisation.
- Fiabilité des recommandations.
- Protection des données personnelles.
- Ressources matérielles limitées.
- Qualité variable des offres historiques.

## 6. Approche retenue

La solution reposera sur les composants suivants :

- Ingestion et traitement des données.
- Recherche hybride dans Qdrant.
- Relations structurées dans Neo4j.
- Orchestration par FastAPI.
- Génération augmentée par LLM.
- Interface web React.

La description détaillée des flux et composants
est disponible dans `architecture.md`.

## 7. Critères de réussite

| Indicateur | Cible prévisionnelle |
|---|---|
| Recall@10 | >= 85 % |
| Recall@5 | >= 80 % |
| Faithfulness | >= 0,85 |
| Answer Relevance | >= 0,80 |
| TTFT | < 800 ms |
| Latence E2E P95 | < 3,5 s |

Ces chiffres sont des objectifs expérimentaux.
Ils n'ont pas encore été mesurés.

Les évaluations devront également porter sur
l'extraction des compétences, leur normalisation
ESCO et la qualité des recommandations.

## 8. Risques et mesures envisagées

| Risque | Mesure d'atténuation |
|---|---|
| Données incomplètes | Détection des informations manquantes |
| Mauvaise normalisation ESCO | Validation des correspondances |
| Hallucinations du LLM | Contexte sourcé et contrôle des réponses |
| Latence élevée | Mesures, optimisation et cache éventuel |
| Données personnelles | Anonymisation et contrôle d'accès |
| Ressources limitées | Déploiement progressif sous Docker |
| Données historiques | Mention explicite de leur période |

## 9. Périmètre du prototype

### Inclus

- Analyse des compétences.
- Référentiel ESCO.
- Recherche documentaire.
- Graphe métiers-compétences.
- Comparaison avec un métier cible.
- Recommandations explicables.
- Interface web de démonstration.

### Hors périmètre initial

- Certification officielle des compétences.
- Recrutement automatique.
- Garantie d'embauche.
- Mise à jour exhaustive et en temps réel
  de toutes les offres du marché.

## 10. Livrables techniques

- Dépôt GitHub structuré.
- Corpus de données représentatif.
- Architecture documentée.
- Comparaison des bases vectorielles.
- Infrastructure Docker initiale.
- Prototype fonctionnel.
- Résultats d'évaluation.

Le projet sera développé progressivement
en fonction des priorités du backlog MoSCoW.
