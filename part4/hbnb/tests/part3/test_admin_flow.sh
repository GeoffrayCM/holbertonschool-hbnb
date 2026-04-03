#!/bin/bash

API="http://127.0.0.1:5000/api/v1"

echo "----- LOGIN ADMIN -----"

ADMIN_TOKEN=$(curl -s -X POST "$API/auth/login" \
-H "Content-Type: application/json" \
-d '{"email":"admin@hbnb.io","password":"admin1234"}' | jq -r '.access_token')

echo "Admin token: $ADMIN_TOKEN"

echo "----- CREATE USER BY ADMIN -----"

USER_RESPONSE=$(curl -s -X POST "$API/users/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-d '{"first_name":"John","last_name":"Doe","email":"john@test.com","password":"secret123"}')

USER_ID=$(echo $USER_RESPONSE | jq -r '.id')

echo "User ID: $USER_ID"

echo "----- LOGIN USER -----"

USER_TOKEN=$(curl -s -X POST "$API/auth/login" \
-H "Content-Type: application/json" \
-d '{"email":"john@test.com","password":"secret123"}' | jq -r '.access_token')

echo "User token: $USER_TOKEN"

echo "----- USER CANNOT CREATE USER (EXPECTED FAIL) -----"

curl -s -o /dev/null -w "%{http_code}\n" \
-X POST "$API/users/" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d '{"first_name":"Hack","last_name":"User","email":"hack@test.com","password":"hack123"}'

echo "----- ADMIN CREATE AMENITY -----"

AMENITY_RESPONSE=$(curl -s -X POST "$API/amenities/" \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d '{"name":"Pool"}')

AMENITY_ID=$(echo $AMENITY_RESPONSE | jq -r '.id')

echo "Amenity ID: $AMENITY_ID"

echo "----- USER CANNOT CREATE AMENITY -----"

curl -s -o /dev/null -w "%{http_code}\n" \
-X POST "$API/amenities/" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d '{"name":"Spa"}'

echo "----- USER CREATE PLACE -----"

PLACE_RESPONSE=$(curl -s -X POST "$API/places/" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"title":"Nice place",
"description":"Test",
"price":100,
"latitude":48.85,
"longitude":2.35,
"owner_id":"fake",
"amenities":[]
}')

PLACE_ID=$(echo $PLACE_RESPONSE | jq -r '.id')

echo "Place ID: $PLACE_ID"

echo "----- USER UPDATE OWN PLACE -----"

curl -s -o /dev/null -w "%{http_code}\n" \
-X PUT "$API/places/$PLACE_ID" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"title":"Updated place",
"description":"Updated",
"price":120,
"latitude":48.85,
"longitude":2.35,
"amenities":[]
}'

echo "----- ADMIN UPDATE USER PLACE -----"

curl -s -o /dev/null -w "%{http_code}\n" \
-X PUT "$API/places/$PLACE_ID" \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"title":"Admin update",
"description":"Admin",
"price":200,
"latitude":48.85,
"longitude":2.35,
"amenities":[]
}'

echo "----- USER CREATE REVIEW -----"

REVIEW_RESPONSE=$(curl -s -X POST "$API/reviews/" \
-H "Authorization: Bearer $USER_TOKEN" \
-H "Content-Type: application/json" \
-d "{
\"text\":\"Great place\",
\"rating\":5,
\"place_id\":\"$PLACE_ID\"
}")

REVIEW_ID=$(echo $REVIEW_RESPONSE | jq -r '.id')

echo "Review ID: $REVIEW_ID"

echo "----- ADMIN UPDATE REVIEW -----"

curl -s -o /dev/null -w "%{http_code}\n" \
-X PUT "$API/reviews/$REVIEW_ID" \
-H "Authorization: Bearer $ADMIN_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"text":"Admin edit",
"rating":4
}'

echo "----- ADMIN DELETE REVIEW -----"

curl -s -o /dev/null -w "%{http_code}\n" \
-X DELETE "$API/reviews/$REVIEW_ID" \
-H "Authorization: Bearer $ADMIN_TOKEN"

echo "----- TEST FINISHED -----"