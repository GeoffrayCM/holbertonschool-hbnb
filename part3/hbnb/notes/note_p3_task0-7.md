# 2. Partie 3 — Task 0

## Modifier l’Application Factory pour gérer la configuration

### Ce que demandait la tâche

La tâche demandait de modifier create_app() pour qu’elle puisse recevoir une classe de configuration.

Exemple attendu :

```python
def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app
```

### Pourquoi cette tâche est importante

Avant cette tâche, on avait un objet Config, mais il n’était pas encore réellement utilisé dans la création de l’application.

Avec cette tâche, on relie enfin :

- l’application Flask
- la configuration
- les futures extensions

---

## Nouvelle notion : Application Factory

L’Application Factory est une fonction qui construit l’application Flask.

Exemple :

```python
def create_app():
    app = Flask(__name__)
    return app
```

### Pourquoi c’est utile :

- permet plusieurs configurations
- facilite les tests
- rend l’app plus modulaire

---

## Nouvelle notion : app.config

app.config est un dictionnaire spécial de Flask qui contient les réglages de l’application.

Exemple :

```python
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"
```

---

## Changement réalisé dans le code

### Avant :

```python
def create_app():
    app = Flask(__name__)
```

### Après :

```python
def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
```

---

## Version type du fichier app/__init__.py

```python
from flask import Flask
from flask_restx import Api

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
```

---

## Ce que cette tâche prépare pour la suite

- SECRET_KEY  
- JWT_SECRET_KEY  
- SQLALCHEMY_DATABASE_URI  
- DEBUG  

---

# 3. Partie 3 — Task 1

## Ajouter le mot de passe au modèle User et le hasher

### Nouvelle notion : Hashing

Un mot de passe ne doit jamais être stocké en clair.

❌ Mauvais :
```python
password = "secret123"
```

✅ Correct :
```python
password = "$2b$12$..."
```

---

## Nouvelle notion : bcrypt

```python
bcrypt.generate_password_hash(password)
bcrypt.check_password_hash(hash, password)
```

---

## Ajout dans app/__init__.py

```python
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

bcrypt.init_app(app)
```

---

## Exemple dans User

```python
def hash_password(self, password):
    from app.extensions import bcrypt
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(self, password):
    from app.extensions import bcrypt
    return bcrypt.check_password_hash(self.password, password)
```

---

## Endpoint POST /users/

```python
user_data = dict(api.payload)
password = user_data.pop("password")

new_user = facade.create_user(user_data)
new_user.hash_password(password)
```

Réponse :

```python
return {
    "id": new_user.id,
    "message": "User successfully created"
}, 201
```

---

# 4. Partie 3 — Task 2

## Authentification JWT

### JWT = JSON Web Token

Authentification **stateless** :

- le client garde le token
- le serveur vérifie à chaque requête

---

## Ajout dans app/__init__.py

```python
from flask_jwt_extended import JWTManager

jwt = JWTManager()
jwt.init_app(app)

app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]
```

---

## Login

```python
user = facade.get_user_by_email(credentials["email"])

if not user or not user.verify_password(credentials["password"]):
    return {"error": "Invalid credentials"}, 401

access_token = create_access_token(
    identity=str(user.id),
    additional_claims={"is_admin": user.is_admin}
)
```

---

## Route protégée

```python
@jwt_required()
def get(self):
    current_user = get_jwt_identity()
    claims = get_jwt()
```

---

# 5. Partie 3 — Task 3

## Ownership & sécurisation

### Différence :

- 401 → non authentifié  
- 403 → non autorisé  

---

## Exemple users.py

```python
@jwt_required()
def put(self, user_id):
    current_user = get_jwt_identity()

    if current_user != user_id:
        return {"error": "Unauthorized action"}, 403

    if "email" in user_data or "password" in user_data:
        return {"error": "You cannot modify email or password."}, 400
```

---

## Exemple places.py

```python
current_user = get_jwt_identity()
place_data["owner_id"] = current_user
```

---

# 6. Partie 3 — Task 4

## RBAC (Role-Based Access Control)

### Helper

```python
from flask_jwt_extended import get_jwt

def is_admin():
    claims = get_jwt()
    return claims.get("is_admin", False)
```

---

## Exemple protection

```python
if not is_admin():
    return {"error": "Admin privileges required"}, 403
```

---

# 7. Swagger + JWT

```python
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add a JWT with ** Bearer <JWT> **'
    }
}
```

---

# 8. SQLAlchemyRepository

```python
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)
```

---

# 9. BaseModel

```python
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
```

---

# 10. User (SQLAlchemy)

```python
email = db.Column(db.String(120), unique=True)
password = db.Column(db.String(128))
is_admin = db.Column(db.Boolean, default=False)
```

---

# 11. Place / Review / Amenity

⚠️ Pas encore de relations :

- pas de ForeignKey
- pas de relationship()

---

# 12. Différences des entités

## User
- auth
- password
- admin

## Amenity
- simple

## Place
- validations métier

## Review
- rating

---

# 13. Facade

```python
self.user_repo = UserRepository()
self.place_repo = SQLAlchemyRepository(Place)
```

---

# 14. Notions clés

- Application Factory
- Config Flask
- Repository Pattern
- Hashing
- JWT
- Ownership
- RBAC
- ORM
- Application Context

---

# 15. Évolution

```
API → Facade → InMemory → dict
API → Facade → SQLAlchemy → SQLite
```

---

# 16. Résultat actuel

- sécurité
- JWT
- hashing
- RBAC
- architecture propre
- base prête

---

# 17. Vision mentale

- JWT → qui es-tu ?
- Ownership → est-ce à toi ?
- Admin → permissions spéciales
- Repository → accès données
- SQLAlchemy → stockage

---

# 18. Étape suivante

Ajouter relations :

- User ↔ Place
- Place ↔ Review
- Place ↔ Amenity

---

# 19. Résumé

## Appris

- structurer une API
- sécuriser
- séparer les responsabilités

## Résultat

- backend propre
- sécurisé
- scalable