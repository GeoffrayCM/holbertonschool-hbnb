Base URL : http://127.0.0.1:5000Base URL : http://127.0.0.1:5000

A) POST create user (OK)
curl -i -X POST http://127.0.0.1:5000/api/v1/users/
-H "Content-Type: application/json"
-d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'

Attendu :

201 Created
JSON avec id + champs
B) POST create user (email déjà utilisé)
curl -i -X POST http://127.0.0.1:5000/api/v1/users/
-H "Content-Type: application/json"
-d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'

Attendu :

400 Bad Request
error: Email already registered
C) POST invalid email
curl -i -X POST http://127.0.0.1:5000/api/v1/users/
-H "Content-Type: application/json"
-d '{"first_name":"John","last_name":"Doe","email":"not-an-email"}'

Attendu :

400 Bad Request (si validation modèle gérée + exceptions attrapées)
error expliquant input invalide
D) GET list users (OK)
curl -i http://127.0.0.1:5000/api/v1/users/

Attendu :

200 OK
liste JSON
E) GET user by id (OK)
curl -i http://127.0.0.1:5000/api/v1/users/USER_ID_HERE

Attendu :

200 OK
F) GET user not found
curl -i http://127.0.0.1:5000/api/v1/users/does-not-exist

Attendu :

404 Not Found
G) PUT update user (OK)
curl -i -X PUT http://127.0.0.1:5000/api/v1/users/USER_ID_HERE
-H "Content-Type: application/json"
-d '{"first_name":"Jane","last_name":"Doe","email":"jane.doe@example.com"}'

Attendu :

200 OK
JSON user mis à jour (ou message selon implémentation)
H) PUT user not found
curl -i -X PUT http://127.0.0.1:5000/api/v1/users/does-not-exist
-H "Content-Type: application/json"
-d '{"first_name":"X","last_name":"Y","email":"x@y.com"}'

Attendu :

404 Not Found
3.3 AMENITIES — Tests cURL
A) POST create amenity (OK)
curl -i -X POST http://127.0.0.1:5000/api/v1/amenities/
-H "Content-Type: application/json"
-d '{"name":"Wi-Fi"}'

Attendu :

201 Created
JSON id + name
B) POST invalid amenity (name vide)
curl -i -X POST http://127.0.0.1:5000/api/v1/amenities/
-H "Content-Type: application/json"
-d '{"name":""}'

Attendu :

400 Bad Request
C) GET list amenities
curl -i http://127.0.0.1:5000/api/v1/amenities/

Attendu :

200 OK
D) GET amenity not found
curl -i http://127.0.0.1:5000/api/v1/amenities/does-not-exist

Attendu :

404 Not Found
E) PUT amenity (OK)
curl -i -X PUT http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID_HERE
-H "Content-Type: application/json"
-d '{"name":"Air Conditioning"}'

Attendu :

200 OK
3.4 PLACES — Tests cURL (relations + bornes)
Pré-requis :

un USER_ID existe (owner)
des AMENITY_ID existent
A) POST create place (OK)
curl -i -X POST http://127.0.0.1:5000/api/v1/places/
-H "Content-Type: application/json"
-d '{ "title":"Cozy Apartment", "description":"A nice place to stay", "price":100.0, "latitude":37.7749, "longitude":-122.4194, "owner_id":"USER_ID_HERE", "amenities":["AMENITY_ID_1","AMENITY_ID_2"] }'

Attendu :

201 Created
B) POST place invalid owner_id
curl -i -X POST http://127.0.0.1:5000/api/v1/places/
-H "Content-Type: application/json"
-d '{ "title":"Bad Place", "description":"x", "price":10.0, "latitude":0.0, "longitude":0.0, "owner_id":"does-not-exist", "amenities":[] }'

Attendu :

400 Bad Request
C) POST place invalid amenity id
curl -i -X POST http://127.0.0.1:5000/api/v1/places/
-H "Content-Type: application/json"
-d '{ "title":"Bad Place", "description":"x", "price":10.0, "latitude":0.0, "longitude":0.0, "owner_id":"USER_ID_HERE", "amenities":["does-not-exist"] }'

Attendu :

400 Bad Request
D) Boundary test latitude > 90
curl -i -X POST http://127.0.0.1:5000/api/v1/places/
-H "Content-Type: application/json"
-d '{ "title":"Bad Lat", "description":"x", "price":10.0, "latitude":91.0, "longitude":0.0, "owner_id":"USER_ID_HERE", "amenities":[] }'

Attendu :

400 Bad Request
E) GET list places (OK)
curl -i http://127.0.0.1:5000/api/v1/places/

Attendu :

200 OK
liste légère (id, title, lat, lon)
F) GET place detail (OK) – enriched
curl -i http://127.0.0.1:5000/api/v1/places/PLACE_ID_HERE

Attendu :

200 OK
owner nested + amenities nested (+ reviews si ajoutée ensuite)
G) PUT update place (OK)
curl -i -X PUT http://127.0.0.1:5000/api/v1/places/PLACE_ID_HERE
-H "Content-Type: application/json"
-d '{ "title":"Luxury Condo", "description":"Updated", "price":200.0, "latitude":37.7749, "longitude":-122.4194, "owner_id":"USER_ID_HERE", "amenities":["AMENITY_ID_1"] }'

Attendu :

200 OK
3.5 REVIEWS — Tests cURL (relations + delete)
Pré-requis :

USER_ID existe
PLACE_ID existe
A) POST create review (OK)
curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/
-H "Content-Type: application/json"
-d '{ "text":"Great place to stay!", "rating":5, "user_id":"USER_ID_HERE", "place_id":"PLACE_ID_HERE" }'

Attendu :

201 Created
review id + fields
B) POST review invalid rating (6)
curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/
-H "Content-Type: application/json"
-d '{ "text":"Bad rating", "rating":6, "user_id":"USER_ID_HERE", "place_id":"PLACE_ID_HERE" }'

Attendu :

400 Bad Request
C) POST review invalid place_id
curl -i -X POST http://127.0.0.1:5000/api/v1/reviews/
-H "Content-Type: application/json"
-d '{ "text":"Bad place", "rating":5, "user_id":"USER_ID_HERE", "place_id":"does-not-exist" }'

Attendu :

400 Bad Request
D) GET list reviews (OK)
curl -i http://127.0.0.1:5000/api/v1/reviews/

Attendu :

200 OK
liste light (id, text, rating)
E) GET review by id (OK)
curl -i http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID_HERE

Attendu :

200 OK
F) GET reviews by place (nested route)
curl -i http://127.0.0.1:5000/api/v1/places/PLACE_ID_HERE/reviews

Attendu :

200 OK
liste des reviews du place
G) DELETE review (OK)
curl -i -X DELETE http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID_HERE

Attendu :

200 OK
message deleted
H) Vérification cohérence après DELETE
curl -i http://127.0.0.1:5000/api/v1/places/PLACE_ID_HERE/reviews

Attendu :

la review supprimée ne doit plus apparaître


## Test swagger:
1) POST /users/ (créer un owner)
2) POST /amenities/ (créer 1 ou 2 amenities)
3) POST /places/ (créer un place avec owner_id + amenities IDs)
4) POST /reviews/ (créer une review avec user_id + place_id)
5) GET /places/<id> (vérifier owner/amenities/reviews)
6) GET /places/<id>/reviews (nested)
7) DELETE /reviews/<id> (vérifier disparition)