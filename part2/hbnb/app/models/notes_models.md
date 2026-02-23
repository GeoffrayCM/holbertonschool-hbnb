# ✅ HBnB — Part 2  
## Task: Implement Core Business Logic Classes

---

# 🎯 Objectif de la tâche

Implémenter la **Business Logic Layer** en créant les classes métier :

- BaseModel
- User
- Place
- Review
- Amenity

Avec :

- UUID pour chaque instance
- created_at / updated_at
- Méthodes save() et update()
- Validations des attributs
- Relations entre entités

But final :  
Avoir une base métier solide avant l’implémentation des endpoints API.

---

# 🧱 Architecture et emplacement des fichiers

Structure :

app/models/
- base_model.py
- user.py
- place.py
- review.py
- amenity.py
- __init__.py

Import standard :

from app.models.base_model import BaseModel

---

# 1️⃣ BaseModel — Rôle Fondamental

## Pourquoi BaseModel ?

Éviter la duplication :

Toutes les entités ont :
- id
- created_at
- updated_at
- save()
- update()

On centralise cette logique.

---

## Attributs

- id : str(uuid.uuid4())
- created_at : datetime.now()
- updated_at : datetime.now()

Pourquoi UUID ?
- Unicité globale
- Sécurité (non prévisible)
- Compatible architecture distribuée

Pourquoi str ?
- Simplifie stockage en mémoire
- Compatible JSON plus tard

---

## Méthodes

### save()
Met à jour updated_at.

### update(data)
- Reçoit un dictionnaire
- Met à jour uniquement les attributs existants
- Appelle save()

---

## Questions orales possibles

Pourquoi ne pas mettre cette logique dans chaque classe ?
→ DRY principle (Don't Repeat Yourself).

Pourquoi update() accepte un dict ?
→ Prépare l'intégration API (PATCH/PUT).

---

# 2️⃣ User — Entité Métier

## Attributs

- id (hérité)
- first_name (requis, max 50)
- last_name (requis, max 50)
- email (requis, format valide, unique)
- is_admin (bool, default False)
- created_at / updated_at

---

## Validations importantes

- Vérification type string
- strip() pour éviter espaces
- Longueur maximale
- Regex pour email
- Bool pour is_admin
- Unicité email via set en mémoire

---

## Pourquoi unicité email ici ?

La tâche l’exige.

En vrai projet :
→ L’unicité serait gérée par la base de données.

Ici :
→ Solution simple en mémoire pour respecter le cahier des charges.

---

## Questions orales

Pourquoi l’unicité ne devrait pas être dans le modèle en production ?
→ Cela appartient à la persistence layer (DB constraint).

Pourquoi valider au niveau modèle ?
→ Protéger la logique métier indépendamment de l’API.

---

# 3️⃣ Amenity — Entité Simple

## Attributs

- id
- name (requis, max 50)
- created_at
- updated_at

Validation :
- string non vide
- longueur ≤ 50

---

# 4️⃣ Place — Entité Centrale

## Attributs

- id
- title (requis, max 100)
- description (optionnel)
- price (float > 0)
- latitude (-90 à 90)
- longitude (-180 à 180)
- owner (User)
- reviews (list)
- amenities (list)
- created_at / updated_at

---

## Relations

### User → Place
Relation one-to-many :
Un User peut posséder plusieurs Place.

Place contient :
owner (instance de User)

---

### Place → Review
Relation one-to-many :
Un Place peut avoir plusieurs Review.

Place contient :
reviews = []

Méthode :
add_review(review)

---

### Place → Amenity
Relation many-to-many simplifiée :
Place contient :
amenities = []

Méthode :
add_amenity(amenity)

---

## Validations critiques

- owner doit être instance User
- price > 0
- latitude et longitude dans range
- types float/int

---

## Questions orales

Pourquoi stocker les relations en listes ?
→ Simplicité avant base de données.

Pourquoi valider owner comme instance User ?
→ Garantir l’intégrité métier.

---

# 5️⃣ Review

## Attributs

- id
- text (requis)
- rating (int 1 à 5)
- place (Place)
- user (User)
- created_at
- updated_at

---

## Validations

- rating entre 1 et 5
- place instance Place
- user instance User

---

## Relations

Review relie :
- un User
- un Place

Place stocke la liste des reviews.

---

# 🧠 Concepts Importants Compris dans cette tâche

## 1) Séparation des responsabilités

Models = logique métier pure  
Pas de HTTP  
Pas de DB  

---

## 2) Validation au niveau métier

On ne dépend pas de l’API pour protéger les données.

Même si quelqu’un crée un objet directement :
→ Les règles sont respectées.

---

## 3) Préparation pour la suite

Ces classes seront utilisées par :

- La Facade
- Le Repository
- Les Endpoints API

---

## 4) Pourquoi pas de logique DB ici ?

Parce que la persistence layer est séparée.

Part 3 → SQLAlchemy remplacera InMemoryRepository.

---

# ⚠️ Points sensibles à connaître à l’oral

- UUID stocké en string
- update() met à jour updated_at
- Unicité email provisoire (en mémoire)
- Relations stockées en listes
- Validation côté modèle
- Héritage BaseModel pour éviter duplication
- Découplage Business / Persistence

---

# 🏁 Résultat attendu de la tâche

À la fin :

- Classes complètes
- Validations fonctionnelles
- Relations opérationnelles
- Tests simples passent
- Prêt pour implémenter l’API

---

# 🎓 Résumé en une phrase

Cette tâche construit le cœur métier de l’application HBnB :  
des entités robustes, validées, liées entre elles, indépendantes de l’API et prêtes à être connectées à la couche persistence et presentation.