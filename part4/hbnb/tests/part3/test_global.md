# 🧪 HBnB API — Test Plan (Swagger + cURL)

---

# 📌 Objectif

Ce document permet de tester entièrement l’API HBnB :

- Authentification (JWT)
- Gestion des users
- Gestion des places
- Gestion des amenities
- Gestion des reviews
- Vérification des relations
- Vérification des règles métier

Tests à faire :
- via **Swagger (interface graphique)**
- via **cURL (ligne de commande)**

---

# ⚙️ Pré-requis

Lancer le serveur :

```bash
python3 run.py
```

Accès :

- API : `http://localhost:5000/api/v1`
- Swagger : `http://localhost:5000/`

---

# 🔐 1. AUTHENTICATION

## 1.1 Login ADMIN (Swagger)

Endpoint : `POST /auth/login`

```json
{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}
```

✅ Attendu :
- Status `200`
- Retour d’un `access_token`

👉 Copier ce token pour la suite

---

## 1.2 Login ADMIN (cURL)

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}'
```

---

# 👤 2. USERS

## 2.1 Créer un user (ADMIN ONLY)

### Swagger
Endpoint : `POST /users/`

```json
{
  "first_name": "Alice",
  "last_name": "Test",
  "email": "alice@test.com",
  "password": "password123"
}
```

Headers :
```
Authorization: Bearer <ADMIN_TOKEN>
```

✅ Attendu :
- Status `201`
- Retour id user

---

### cURL

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
-H "Authorization: Bearer <ADMIN_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Alice",
  "last_name": "Test",
  "email": "alice@test.com",
  "password": "password123"
}'
```

---

## 2.2 Récupérer les users

```bash
curl http://localhost:5000/api/v1/users/
```

✅ Attendu :
- Liste des users

---

## 2.3 Récupérer un user

```bash
curl http://localhost:5000/api/v1/users/<USER_ID>
```

---

## 2.4 Update user

```bash
curl -X PUT http://localhost:5000/api/v1/users/<USER_ID> \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Updated"
}'
```

---

# 🏠 3. AMENITIES

## 3.1 Créer une amenity

```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
-H "Authorization: Bearer <ADMIN_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "name": "WiFi"
}'
```

---

## 3.2 Lister amenities

```bash
curl http://localhost:5000/api/v1/amenities/
```

---

# 🏡 4. PLACES

## 4.1 Créer une place

```bash
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Authorization: Bearer <USER_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "title": "My Place",
  "description": "Nice place",
  "price": 100,
  "latitude": 48.85,
  "longitude": 2.35,
  "amenities": ["<AMENITY_ID_1>", "<AMENITY_ID_2>"]
}'
```

✅ Attendu :
- Place créée
- owner = user connecté

---

## 4.2 Lire une place

```bash
curl http://localhost:5000/api/v1/places/<PLACE_ID>
```

✅ Vérifier :
- owner
- amenities

---

## 4.3 Update place

```bash
curl -X PUT http://localhost:5000/api/v1/places/<PLACE_ID> \
-H "Authorization: Bearer <USER_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "price": 150
}'
```

---

# ⭐ 5. REVIEWS

## 5.1 Créer review (user différent du owner)

```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
-H "Authorization: Bearer <USER2_TOKEN>" \
-H "Content-Type: application/json" \
-d '{
  "text": "Great place",
  "rating": 5,
  "place_id": "<PLACE_ID>"
}'
```

---

## 5.2 Lire review

```bash
curl http://localhost:5000/api/v1/reviews/<REVIEW_ID>
```

---

## 5.3 Lire reviews d’une place

```bash
curl http://localhost:5000/api/v1/places/<PLACE_ID>/reviews
```

---

# 🔗 6. TEST DES RELATIONS

## Vérifier :

### Place → Owner
- `GET /places/<id>`
- vérifier user lié

### Place → Amenities
- vérifier liste amenities

### Place → Reviews
- vérifier reviews remontent

### Review → User
- vérifier auteur du review

---

# ❌ 7. TESTS NÉGATIFS

## 7.1 User review sa propre place

```bash
POST /reviews
```

❌ Attendu :
- 400 ou 403

---

## 7.2 Double review même user/place

❌ Attendu :
- erreur UNIQUE

---

## 7.3 Email déjà existant

❌ Attendu :
- erreur 400

---

## 7.4 Mauvais login

```bash
POST /auth/login
```

❌ Attendu :
- 401

---

# 🧹 8. CLEANUP (optionnel)

Supprimer :
- reviews
- places
- users test

(selon endpoints dispo)

---

# ✅ RÉSULTAT FINAL ATTENDU

Si tout est correct :

- Auth fonctionne
- Permissions admin / user OK
- Relations OK :
  - User ↔ Place
  - Place ↔ Amenity
  - Place ↔ Review
  - User ↔ Review
- Contraintes respectées :
  - 1 review / user / place
  - pas son propre logement
  - email unique

---

# 🎯 CONCLUSION

Si tous ces tests passent :
👉 votre API est fonctionnelle, cohérente et conforme au modèle HBnB.