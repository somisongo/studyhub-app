# Architecture du Système StudyHub

## Vue d'ensemble

StudyHub est conçu selon une architecture moderne de microservices, permettant une évolutivité et une maintenance optimales. Le système est divisé en plusieurs composants qui communiquent entre eux via des API REST et des messages asynchrones.

## Diagramme d'Architecture

```
+---------------------+     +----------------------+     +----------------------+
|                     |     |                      |     |                      |
|  Application Web    |     |  Application Mobile  |     |      API Gateway    |
|    (React.js)       |<--->|      (Flutter)       |<--->|      (FastAPI)      |
|                     |     |                      |     |                      |
+---------------------+     +----------------------+     +----------+-----------+
                                                                   |
                                                                   |
                            +--------------------------------+     |
                            |                                |     |
                            |        Service Bus / MQ        |<----+
                            |        (RabbitMQ)             |     |
                            |                                |     |
                            +--+--------+--------+--------+--+     |
                               |        |        |        |        |
                               v        v        v        v        v
+---------------+    +----------+  +----------+  +----------+  +----------+
|               |    |          |  |          |  |          |  |          |
| Base Données  |<-->|  Service |  |  Service |  |  Service |  |  Service |
| (PostgreSQL/  |    |   Notes  |  |   OCR    |  |   NLP    |  |   Auth   |
|  MongoDB)     |    |          |  |          |  |          |  |          |
|               |    |          |  |          |  |          |  |          |
+---------------+    +----------+  +----------+  +----------+  +----------+
```

## Composants Principaux

### Frontends
1. **Application Web (React.js)**
   - Interface utilisateur web responsive
   - Éditeur de notes riche
   - Visualisations et tableaux de bord

2. **Application Mobile (Flutter)**
   - Version mobile de l'application
   - Fonctionnalités de capture rapide
   - Notifications push
   - Mode hors ligne

### Backend
1. **API Gateway (FastAPI)**
   - Point d'entrée unique pour les clients
   - Routage des requêtes vers les services appropriés
   - Gestion de l'authentification
   - Mise en cache et limitation de débit

2. **Service Bus / Message Queue (RabbitMQ)**
   - Communication asynchrone entre services
   - File d'attente pour les tâches intensives en ressources
   - Garantie de livraison des messages

3. **Microservices**
   - **Service de Notes**
     - Gestion des notes et de leur organisation
     - Versionnage et historique des modifications
     - Système de tags et métadonnées

   - **Service OCR**
     - Conversion des images en texte
     - Reconnaissance d'écriture manuscrite
     - Détection et extraction de structures (tableaux, formules)

   - **Service NLP**
     - Analyse de texte et extraction de mots-clés
     - Génération de résumés
     - Création de questions pour tests
     - Classification et catégorisation automatique

   - **Service d'Authentification**
     - Gestion des utilisateurs et des rôles
     - Authentification et autorisation
     - Gestion des sessions et tokens JWT

### Stockage
1. **PostgreSQL**
   - Données structurées (utilisateurs, métadonnées, relations)
   - Transactions ACID
   - Recherche full-text

2. **MongoDB**
   - Stockage des notes et contenus riches
   - Données non structurées et documents JSON
   - Évolutivité horizontale

## Flux de Données

1. **Création d'une Note**
   - L'utilisateur crée une note via l'interface web/mobile
   - La requête est envoyée à l'API Gateway
   - Le Service de Notes traite et enregistre la note
   - Des tâches d'analyse sont mises en file d'attente dans RabbitMQ
   - Le Service NLP traite la note pour extraire des mots-clés et générer un résumé
   - Les résultats sont stockés et renvoyés à l'utilisateur

2. **Capture d'Image/OCR**
   - L'utilisateur prend une photo d'un document
   - L'image est envoyée au Service OCR via l'API Gateway
   - Le texte extrait est renvoyé et inséré dans une nouvelle note
   - Le Service de Notes traite et enregistre la note

3. **Révision Planifiée**
   - Le système planifie des révisions selon la courbe de l'oubli
   - À l'heure planifiée, une notification est envoyée
   - L'utilisateur accède à la révision
   - Le Service NLP génère des questions basées sur les notes
   - Les résultats de la révision sont utilisés pour ajuster le planning futur

## Considérations Techniques

1. **Scalabilité**
   - Tous les services sont dockerisés
   - Déploiement sur Kubernetes pour l'auto-scaling
   - Services sans état pour faciliter la réplication

2. **Sécurité**
   - Chiffrement des données en transit (HTTPS)
   - Chiffrement des données sensibles au repos
   - Authentification basée sur JWT avec rotation des clés
   - Validation stricte des entrées utilisateur

3. **Résilience**
   - Circuit breakers entre services
   - Retry policies pour les opérations temporairement défaillantes
   - Surveillance et alertes en temps réel
   - Sauvegarde régulière des données