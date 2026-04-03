# 🧠 FICHE DE RÉVISION — SQLAlchemy Relationships (HBnB Part 3)

---

## 🎯 Objectif de la tâche

Mettre en place les **relations entre les entités** du projet HBnB avec SQLAlchemy afin de :

- structurer les données
- garantir l'intégrité
- permettre des requêtes simples et puissantes
- refléter la logique métier réelle

---

## 🧩 Rappel des entités

- User
- Place
- Review
- Amenity

---

## 🔗 Relations implémentées

### 1. User ↔ Place (One-to-Many)

```
User (1) -------- (N) Place
```

- Un utilisateur peut posséder plusieurs places
- Une place appartient à un seul utilisateur

### Implémentation

#### Place

```python
user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

owner = db.relationship("User", backref="places", lazy=True)
```

### Utilisation

```python
place.owner        # récupère le User
user.places        # récupère toutes les places
```

---

### 2. Place ↔ Review (One-to-Many)

```
Place (1) -------- (N) Review
```

- Une place peut avoir plusieurs reviews
- Une review concerne une seule place

#### Review

```python
place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

place = db.relationship("Place", backref="reviews", lazy=True)
```

### Utilisation

```python
review.place       # accès à la place
place.reviews      # liste des reviews
```

---

### 3. User ↔ Review (One-to-Many)

```
User (1) -------- (N) Review
```

- Un utilisateur peut écrire plusieurs reviews
- Une review appartient à un seul utilisateur

#### Review

```python
user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

user = db.relationship("User", backref="reviews", lazy=True)
```

### Utilisation

```python
review.user        # récupère l'auteur
user.reviews       # récupère ses reviews
```

---

### 4. Place ↔ Amenity (Many-to-Many)

```
Place (N) -------- (N) Amenity
        via place_amenity
```

- Une place peut avoir plusieurs équipements
- Un équipement peut appartenir à plusieurs places

---

## 🧱 Table d'association

```python
place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)
```

---

## 🔗 Relation ORM

```python
amenities = db.relationship(
    "Amenity",
    secondary=place_amenity,
    lazy="subquery",
    backref=db.backref("places", lazy=True)
)
```

---

## 📌 Utilisation

```python
place.amenities        # liste des amenities
amenity.places         # liste des places
```

---

## ⚙️ SQLAlchemy — notions clés

---

### 🔑 ForeignKey

Permet de lier une table à une autre :

```python
db.ForeignKey("users.id")
```

➡️ signifie :
"cette colonne pointe vers users.id"

---

### 🔁 relationship()

Permet d'accéder aux objets liés en Python

```python
db.relationship("User", backref="places")
```

➡️ SQLAlchemy crée automatiquement :

- `place.owner`
- `user.places`

---

### 🔄 backref

Crée automatiquement la relation inverse

```python
backref="places"
```

➡️ évite d'écrire deux fois la relation

---

### 💤 lazy loading

Contrôle quand les données sont chargées

- `lazy=True` → chargement à l'accès
- `lazy="subquery"` → chargement optimisé en une requête

---

## 🧠 Logique métier implémentée

---

### ❌ Interdiction de review sa propre place

```python
if place.user_id == user.id:
    raise ValueError("Cannot review your own place")
```

---

### ❌ Un seul review par user/place

```python
existing_reviews = place.reviews
for review in existing_reviews:
    if review.user_id == user.id:
        raise ValueError("User already reviewed this place")
```

---

## 🏗️ Flux complet d’une requête

---

### Création d'une place

```
HTTP JSON
   ↓
API (places.py)
   ↓
Facade
   ↓
Model (Place)
   ↓
SQLAlchemy
   ↓
Database
```

---

### Exemple concret

```python
place = Place(...)
place.amenities.append(amenity)
db.session.add(place)
db.session.commit()
```

---

## 🧪 Tests validés

✔ création user  
✔ login  
✔ création amenities  
✔ création place avec amenities  
✔ lecture relations  
✔ création review  
✔ validation contraintes  

---

## 🧨 Bug rencontré (important)

### ❌ Erreur

```
AttributeError: 'Place' object has no attribute 'amenities'
```

### 🧠 Cause

- mauvais fichier chargé
- ou relation non définie dans le modèle réellement importé

### ✅ Solution

- vérifier avec :

```bash
python3 -c "from app.models.place import Place; print(hasattr(Place, 'amenities'))"
```

---

## 🧠 Ce qu’il faut retenir

---

### SQLAlchemy sert à :

- mapper objets Python ↔ tables SQL
- simplifier les requêtes
- gérer les relations automatiquement

---

### Les relations permettent :

- d’éviter les jointures SQL manuelles
- d’avoir un code lisible
- de manipuler des objets liés naturellement

---

### Résumé des relations

```
User ────< Place ────< Review
  │                        ▲
  └────────────<───────────┘

Place ────<────>──── Amenity
```

---

## 🚀 Conclusion

- Toutes les relations sont fonctionnelles
- Le mapping ORM est correctement mis en place
- Les règles métier sont respectées
- Le projet est prêt pour la suite

---
