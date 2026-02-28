# Fiche de révision – HBnB Part 2 (Business Logic + API)

## 0) Objectif global de la Part 2

Cette partie met en place une application API fonctionnelle (sans base de données, sans authentification) en respectant une architecture propre :

- Une structure de projet modulaire (packages Python)
- Une séparation en couches :
  - Presentation Layer (API Flask-RESTx)
  - Business Logic Layer (Models + règles métier)
  - Persistence Layer (Repository in-memory)
- Une communication centralisée via le Facade Pattern

Le résultat attendu est une API REST qui gère progressivement :
- Users (POST/GET/PUT + GET list)
- Amenities (POST/GET/PUT + GET list)
- Places (POST/GET/PUT + GET list) avec relations (owner + amenities)
- Reviews (POST/GET/PUT/DELETE + GET list + GET by place) avec relations (user + place) et intégration côté places

---

## 1) Architecture en couches (Layered Architecture)

### 1.1 Présentation (API)
Responsable de :
- Recevoir les requêtes HTTP (GET/POST/PUT/DELETE)
- Valider la structure du JSON d’entrée (types/champs requis via RESTx)
- Appeler la façade (et uniquement la façade)
- Transformer les objets en JSON (sérialisation)
- Renvoyer des codes HTTP cohérents (200/201/400/404)

Point clé : l’API n’accède pas directement au stockage.

### 1.2 Logique métier (Business Logic)
Responsable de :
- Représenter les entités du domaine (User, Place, Amenity, Review)
- Contenir les règles métier (validations, contraintes, relations)
- Assurer l’intégrité des données lors des modifications

Exemple concret :
- Un User doit avoir un email valide, un prénom/nom non vides, longueur max.
- Une Place doit avoir des coordonnées valides, un prix non négatif.
- Une Review doit avoir un rating entre 1 et 5 et être liée à un user et un place existants.

### 1.3 Persistance (Repository)
Responsable de :
- Stocker et récupérer les objets
- Offrir une interface stable (contrat Repository)
- Être remplaçable plus tard (SQLAlchemy en Part 3)

Actuellement : InMemoryRepository (dict interne) qui stocke par id.

---

## 2) Pourquoi Repository + Interface Repository

### 2.1 Repository (concept)
Un Repository est une couche d’accès aux données :
- add(obj)
- get(id)
- get_all()
- update(id, data)
- delete(id)
- get_by_attribute(name, value)

### 2.2 Interface Repository (contrat)
Une interface (classe abstraite) impose les mêmes méthodes quel que soit le backend (mémoire, SQL, etc.).

Idée clé : le reste du code dépend d’un contrat, pas d’une implémentation.

Conséquence :
- La façade et les modèles ne changent presque pas quand la persistence change.
- Part 3 remplacera InMemoryRepository sans devoir réécrire tous les endpoints.

---

## 3) Facade Pattern (HBnBFacade)

### 3.1 Définition
Le Facade Pattern fournit une interface unique et simplifiée à un sous-système.

Dans le projet :
- L’API appelle uniquement la façade.
- La façade orchestre : validations relationnelles, création d’objets, stockage, mise à jour.

### 3.2 Pourquoi c’est utile ici
- Centralise la logique de coordination (API reste simple)
- Empêche l’API de manipuler directement les repositories
- Facilite l’évolution (persistence DB, auth, rôles)

### 3.3 Singleton de façade
Une instance unique de façade est créée dans `app/services/__init__.py` :

- Toute l’application utilise le même stockage in-memory.
- Si plusieurs instances existaient, chacune aurait son propre stockage, ce qui casserait la cohérence :
  - un user créé dans une façade ne serait pas visible depuis une autre façade.

---

## 4) Flask, Flask-RESTx, Swagger (concret)

### 4.1 Flask
Flask est le serveur web :
- reçoit les requêtes HTTP
- route les requêtes vers les handlers
- renvoie la réponse HTTP

### 4.2 Flask-RESTx
Flask-RESTx est une extension spécialisée API REST :
- Namespace : regroupe les routes par ressource (`users`, `places`, etc.)
- Resource : classe qui contient `get/post/put/delete`
- api.model : modèle de doc et validation d’entrée
- Génère automatiquement Swagger / OpenAPI

### 4.3 Swagger
Swagger est l’interface web interactive de documentation générée automatiquement :
- liste les endpoints
- montre les modèles attendus
- permet de tester via “Try it out”

Important : Swagger n’écrit pas la logique. Il expose ce qui est déclaré via RESTx.

---

## 5) Structure du projet (sens et pièges)

Structure typique :

- app/__init__.py : application factory `create_app()`, enregistre les namespaces
- app/api/v1/*.py : endpoints REST (presentation layer)
- app/models/*.py : classes métier + validations
- app/services/facade.py : orchestration (façade)
- app/persistence/repository.py : interface + InMemoryRepository
- run.py : point d’entrée (lance create_app)

Pièges fréquents :
- Ajouter `api.add_namespace(...)` sans importer le namespace (NameError)
- Import circulaire (API import facade, facade import models, models import facade) : éviter que les models importent l’API ou la façade
- Oublier le slash final dans certaines routes ou utiliser des placeholders dans curl (`<id>` avec chevrons)
- Réponses JSON incohérentes selon endpoints (important pour tests et oral)

---

## 6) Modèles (Models) : héritage, validations, relations

### 6.1 BaseModel (héritage)
Les entités héritent d’un BaseModel qui fournit :
- id (UUID string)
- created_at
- updated_at
- save() : met à jour updated_at
- update(data) : met à jour les champs autorisés puis save()

Héritage = réutilisation logique :
- Les règles communes (timestamps, id, update) n’ont pas à être copiées dans chaque classe.

### 6.2 User
Règles métier typiques :
- first_name / last_name : requis, longueur max, nettoyage (strip)
- email : requis, format email via regex
- is_admin : bool par défaut False

Point important :
- La validation fine ne doit pas être laissée uniquement à RESTx (RESTx valide surtout structure, pas logique métier).

### 6.3 Amenity
Simple :
- name : requis, longueur max éventuelle
- pas de relation directe imposée ici (relation portée par Place)

### 6.4 Place
Spécificités majeures :
- Validation numérique :
  - price >= 0
  - latitude entre -90 et 90
  - longitude entre -180 et 180
- Relations :
  - owner : un User (one-to-many : un user possède plusieurs places)
  - amenities : liste d’Amenity (many-to-many)

Point important :
- L’API reçoit owner_id et amenities (liste d’IDs) mais le modèle Place manipule des objets (owner, amenity objects).
- Conversion ID → objets se fait idéalement dans la façade (pas dans l’API).

### 6.5 Review
Spécificités majeures :
- rating : entier entre 1 et 5
- text : requis
- relations obligatoires :
  - user : User existant
  - place : Place existante

Review est aussi l’unique entité avec DELETE dans Part 2.

---

## 7) Endpoints : ce qui a été implémenté et pourquoi

### 7.1 Users
- POST /users : crée un user, vérifie unicité email (via get_by_attribute)
- GET /users : liste de users
- GET /users/<id> : détail
- PUT /users/<id> : update

Piège : GET list ne doit pas lire api.payload (pas de body en GET).

### 7.2 Amenities
- POST /amenities
- GET /amenities
- GET /amenities/<id>
- PUT /amenities/<id>

Différence vs User : pas d’unicité imposée.

### 7.3 Places
- POST /places : exige owner_id et amenities (ids) et valide les relations
- GET /places : liste “light” (id, title, latitude, longitude)
- GET /places/<id> : détail enrichi (owner + amenities, plus tard reviews)
- PUT /places/<id> : update (avec gestion owner_id et amenities)

Pièges :
- Accepter que amenities soit une liste d’IDs (input), mais renvoyer amenities comme objets (output enrichi).
- Ne pas inclure reviews dans cette étape initiale (avant task review).

### 7.4 Reviews
- POST /reviews : valide user_id + place_id + rating, crée review, l’attache à la place
- GET /reviews : liste “light”
- GET /reviews/<id> : détail complet
- PUT /reviews/<id> : update (sans changer user_id/place_id si choisi)
- DELETE /reviews/<id> : supprime, et enlève de place.reviews
- GET /places/<place_id>/reviews : route sous namespace places

Pièges :
- L’endpoint nested doit être dans places.py (pas reviews.py).
- Lors d’un delete, retirer la review du repo mais aussi de la collection place.reviews (sinon incohérence).

---

## 8) Sérialisation (JSON) et données liées

### 8.1 Pourquoi sérialiser
Les clients ne comprennent pas les objets Python.
Il faut transformer en dictionnaires JSON.

### 8.2 Sérialisation simple vs enrichie
Exemples :
- GET /places (list) : réponse légère (résumé)
- GET /places/<id> : réponse enrichie (owner + amenities + reviews)

Approche recommandée :
- Avoir une fonction utilitaire `place_to_dict(place, include_owner, include_amenities, include_reviews)`
- Avoir une fonction `review_to_dict(review, include_relations)`

Piège :
- Confondre modèle RESTx (documentation) et contenu renvoyé réellement : RESTx n’impose pas tout seul le contenu de la réponse.

---

## 9) Circulation dans le code : exécutions typiques (le flux)

### 9.1 Création d’un User (POST /api/v1/users/)
1) Client envoie JSON (first_name, last_name, email)
2) RESTx valide la structure (required, types) si validate=True
3) La méthode post() du Resource est appelée
4) API appelle facade.get_user_by_email(email)
5) Facade lit dans user_repo (InMemoryRepository)
6) Si ok, API appelle facade.create_user(user_data)
7) Facade instancie User(**data) → validation dans le modèle
8) Facade ajoute au repo (user_repo.add)
9) API sérialise l’objet et retourne 201

Points où ça peut échouer :
- validation RESTx (champs manquants) → 400
- email déjà existant → 400
- validation modèle (format email, longueurs) → 400 si exceptions gérées

### 9.2 Création d’une Place (POST /api/v1/places/)
1) Client envoie JSON (title, price, latitude, longitude, owner_id, amenities=[ids])
2) RESTx valide structure
3) API appelle facade.create_place(place_data)
4) Facade récupère owner via user_repo.get(owner_id)
   - si None → erreur (400)
5) Facade récupère chaque amenity via amenity_repo.get(id)
   - si un id invalide → erreur (400)
6) Facade crée Place(... owner=UserObject ...)
   - validation dans Place (price/lat/lon)
7) Facade attache les amenities (place.add_amenity)
8) Facade stocke place dans place_repo
9) API retourne 201

Pièges :
- Confondre owner_id (input) et owner (objet)
- Ne pas gérer amenities invalides
- Validation (lat/long hors bornes)

### 9.3 Création d’une Review (POST /api/v1/reviews/) : cas plus complexe
1) Client envoie JSON (text, rating, user_id, place_id)
2) RESTx valide structure
3) API appelle facade.create_review(review_data)
4) Facade récupère user via user_repo.get(user_id) sinon 400
5) Facade récupère place via place_repo.get(place_id) sinon 400
6) Facade crée Review(text, rating, user=UserObject, place=PlaceObject)
   - validation rating 1..5
7) Facade stocke la review dans review_repo
8) Facade attache la review à la place : place.add_review(review)
9) API retourne 201 avec id/text/rating/user_id/place_id

Pourquoi attacher à Place :
- pour que GET /places/<place_id>/reviews fonctionne
- pour que GET /places/<id> puisse inclure la liste des reviews

Pièges :
- Oublier l’attachement place.add_review
- Supprimer une review du repo sans la retirer de place.reviews

### 9.4 Récupérer les reviews d’une place (GET /places/<id>/reviews)
1) API places.py reçoit place_id
2) Appelle facade.get_reviews_by_place(place_id)
3) Facade récupère la place (place_repo.get)
   - si None → API retourne 404
4) Sinon renvoie place.reviews
5) API renvoie liste sérialisée (id/text/rating)

---

## 10) Gestion d’erreurs (400 vs 404) : repères

- 400 Bad Request :
  - JSON invalide (structure, types, required)
  - owner_id invalide lors d’un POST place (input incorrect)
  - amenity_id invalide
  - user_id/place_id invalide lors d’un POST review
  - rating invalide

- 404 Not Found :
  - GET /resource/<id> quand la ressource n’existe pas
  - PUT /resource/<id> quand la ressource n’existe pas
  - DELETE /reviews/<id> quand la review n’existe pas
  - GET /places/<place_id>/reviews quand place_id n’existe pas

Piège : Mélanger 400 et 404 sur les relations.
Règle pratique :
- ressource demandée par URL et inexistante → 404
- ressource référencée dans un payload et invalide → 400

---

## 11) Tests : outils et méthodes efficaces

### 11.1 curl
- permet de tester rapidement endpoints + status codes
- attention aux chevrons : ne jamais mettre `<id>` dans l’URL, remplacer par un vrai id

### 11.2 Swagger UI
- utile pour explorer et tester rapidement
- reflète la doc RESTx (models, responses)
- ne remplace pas les tests en ligne de commande

### 11.3 Stratégie de test
- Tester d’abord l’ordre logique :
  - créer user
  - créer amenities
  - créer place
  - créer review
- Tester ensuite :
  - get list
  - get by id
  - put
  - delete
- Tester les erreurs :
  - ids inexistants
  - rating hors limite
  - lat/long invalides

Piège : In-memory repo est vidé à chaque redémarrage de serveur.

---

## 12) Points confus classiques et pièges 

- Confondre Flask et RESTx :
  - Flask = serveur et routage
  - RESTx = structure Resource/Namespace + doc + validation basique + swagger

- Confondre validation RESTx et validation métier :
  - RESTx valide la forme (champs requis)
  - Les modèles valident le fond (formats, bornes, règles métier)

- Import/namespace :
  - `api = Namespace(...)` doit exister dans chaque fichier endpoint
  - `api.add_namespace(...)` dans create_app doit importer correctement le namespace, sinon NameError/ImportError

- Relations :
  - owner_id dans JSON n’est pas owner objet
  - amenities en entrée sont des IDs, en sortie ce sont des objets sérialisés
  - review doit être attachée à place pour les routes nested

- DELETE review :
  - supprimer uniquement du repo crée un état incohérent si place.reviews n’est pas mis à jour

- Application factory :
  - create_app() dans app/__init__.py est essentiel pour config/tests futurs

---

## 13) Conclusion 

La Part 2 construit une API REST structurée et scalable en séparant clairement :
- l’API (presentation)
- la logique métier (models + validations)
- la persistance (repository in-memory)

Le Facade Pattern centralise toutes les interactions entre ces couches.
Les entités simples (User/Amenity) servent de base.
Les entités relationnelles (Place/Review) introduisent la validation de relations, la sérialisation enrichie et la cohérence des collections (amenities, reviews).
Review est la seule entité avec DELETE, ce qui oblige à gérer la cohérence entre repository et relations in-memory.

Cette architecture prépare la transition vers une base de données et une authentification dans les parties suivantes.
