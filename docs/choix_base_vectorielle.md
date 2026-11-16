
# Choix de la base vectorielle — PathForge AI

## 1. Contexte de la décision

PathForge AI nécessite une base vectorielle
pour indexer et retrouver les passages documentaires
provenant des CV, projets et offres d'emploi.

Les besoins principaux sont :

- Recherche sémantique.
- Recherche hybride dense et lexicale.
- Filtrage par métadonnées.
- Récupération rapide des candidats.
- Déploiement local simple.
- Intégration avec Python et FastAPI.

Trois solutions sont étudiées :

1. Qdrant.
2. Milvus.
3. PostgreSQL avec pgvector.

## 2. Critères de comparaison

### Recherche vectorielle

La base doit permettre l'indexation
et la recherche des embeddings.

### Recherche hybride

Le système doit combiner recherche dense
et recherche lexicale de type BM25.

### Filtrage par métadonnées

Les recherches doivent pouvoir utiliser :

- Source documentaire.
- Type de document.
- Identifiant du métier.
- Identifiant du profil.
- Référence ESCO, si applicable.

### Performance

La latence des requêtes et la capacité
à gérer l'augmentation du corpus sont importantes.

### Exploitation locale

La solution doit être utilisable
sur les machines de développement de l'équipe.

## 3. Tableau comparatif

| Critère | Qdrant | Milvus | pgvector |
|---|---|---|---|
| Recherche vectorielle | Native | Native | Extension PostgreSQL |
| HNSW | Oui | Oui | Oui |
| Filtrage de métadonnées | Payload filtering | Filtrage scalaire | SQL WHERE |
| Recherche hybride | Dense et sparse | Plusieurs possibilités hybrides | Combinaison SQL et recherche vectorielle |
| Déploiement local | Simple avec Docker | Potentiellement plus complexe | Simple si PostgreSQL existe |
| Intégration Python | SDK dédié | SDK dédié | Écosystème PostgreSQL |
| Complexité opérationnelle | Modérée | Variable selon le mode | Faible à modérée |
| Usage privilégié | Recherche vectorielle applicative | Recherche vectorielle évolutive | Recherche intégrée à SQL |

## 4. Analyse des solutions

### Qdrant

Points forts :

- API dédiée aux recherches vectorielles.
- Support des vecteurs denses et sparse.
- Filtrage des payloads.
- Indexation HNSW.
- Client Python.
- Déploiement local direct avec Docker.

Limites :

- Service supplémentaire à maintenir.
- Nécessité de coordonner les données
  avec PostgreSQL et Neo4j.

### Milvus

Points forts :

- Moteur spécialisé pour la recherche vectorielle.
- Plusieurs stratégies d'indexation.
- Possibilités de montée en charge.
- Fonctions de recherche hybride.

Limites :

- Exploitation potentiellement plus complexe
  selon l'architecture de déploiement.
- Surdimensionnement possible pour un premier prototype.

### pgvector

Points forts :

- Intégration directe dans PostgreSQL.
- Requêtes SQL et filtres relationnels.
- Infrastructure simplifiée si PostgreSQL
  est déjà le stockage principal.

Limites :

- Mise en place hybride potentiellement plus manuelle.
- Gestion conjointe des charges relationnelles
  et vectorielles dans le même système.

## 5. Décision retenue

**Base vectorielle sélectionnée : Qdrant.**

Ce choix est principalement motivé par :

1. Son adaptation à la recherche hybride.
2. Le filtrage sur les métadonnées.
3. Sa simplicité de déploiement local.
4. L'intégration avec Python et FastAPI.
5. La séparation claire des responsabilités
   entre stockage vectoriel et stockage relationnel.

Neo4j restera responsable des relations du graphe.

PostgreSQL conservera les données applicatives.

Qdrant gérera la récupération documentaire.

## 6. Validation locale

Configuration actuelle :

- Image Docker : `qdrant/qdrant:v1.15.5`.
- Port REST : 6333.
- Port gRPC : 6334.
- Stockage persistant : volume Docker.

Commandes :

    docker compose up -d

    docker compose ps

Tableau de bord :

http://localhost:6333/dashboard

Le démarrage local et l'accès au tableau de bord
ont été vérifiés.

Cela confirme la disponibilité du service,
mais pas encore les performances de recherche.

## 7. Protocole de benchmark prévu

Les trois solutions devront être évaluées,
si les ressources et le temps le permettent,
sur un même corpus et des requêtes identiques.

Mesures envisagées :

- Temps moyen de recherche.
- Latence P95.
- Recall@10.
- Effet des filtres de métadonnées.
- Consommation mémoire.
- Facilité d'exploitation.

Les volumes, paramètres d'indexation
et conditions matérielles seront documentés.

Aucun résultat comparatif de latence
n'est annoncé à ce stade.

## 8. Conclusion

Qdrant représente le compromis retenu
pour le prototype PathForge AI.

Il fournit les mécanismes utiles
à la récupération vectorielle et hybride
sans imposer une infrastructure trop lourde.

Ce choix sera réévalué si les benchmarks
ou les contraintes du projet le justifient.
