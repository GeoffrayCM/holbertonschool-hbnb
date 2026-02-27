
        #test get user list

curl -i -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'

curl -i -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"jane.doe@example.com"}'

curl -i http://127.0.0.1:5000/api/v1/users/

expected :
[
  {"id":"...","first_name":"John","last_name":"Doe","email":"john.doe@example.com"},
  {"id":"...","first_name":"Jane","last_name":"Doe","email":"jane.doe@example.com"}
]


            # TEST PUT (update user)
(crée user)
curl -i -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'

USER_ID="COLLE_ID_ICI"

(update)
curl -i -X PUT "http://127.0.0.1:5000/api/v1/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"jane.doe@example.com"}'

(verif get by id)
curl -i "http://127.0.0.1:5000/api/v1/users/$USER_ID"

(verif user inexistant)
curl -i -X PUT http://127.0.0.1:5000/api/v1/users/does-not-exist \
  -H "Content-Type: application/json" \
  -d '{"first_name":"X","last_name":"Y","email":"x@y.com"}'