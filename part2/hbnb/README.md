# 🧠 Business Logic Layer – Core Entities

## 📌 Overview

The Business Logic layer defines the core entities of the HBnB application and enforces the rules that govern their behavior.  

All entities inherit from a common `BaseModel` class, which provides:

- A unique UUID identifier (`id`)
- Creation timestamp (`created_at`)
- Update timestamp (`updated_at`)
- A `save()` method to refresh `updated_at`
- An `update(data)` method to safely update attributes

The entities implemented in this task are:

- `User`
- `Place`
- `Review`
- `Amenity`

---

# 🏗 BaseModel

## Responsibilities

- Generate a unique UUID (`str(uuid.uuid4())`)
- Track object creation and modification time
- Provide a generic update mechanism
- Protect critical attributes (`id`, `created_at`, `updated_at`) from modification

## Core Methods

- `save()` → updates `updated_at`
- `update(data: dict)` → updates existing attributes safely

---

# 👤 User

## Attributes

| Attribute | Type | Constraints |
|------------|--------|------------|
| id | String | UUID |
| first_name | String | Required, max 50 characters |
| last_name | String | Required, max 50 characters |
| email | String | Required, valid email format |
| is_admin | Boolean | Default: False |
| created_at | DateTime | Auto-generated |
| updated_at | DateTime | Auto-updated |

## Responsibilities

- Validate name length and presence
- Validate email format using regular expressions
- Ensure `is_admin` is boolean
- Handle safe updates via `update()`

## Example Usage

```python
from app.models.user import User

user = User("John", "Doe", "john.doe@example.com")
print(user.id)
print(user.created_at)

user.update({"first_name": "Jane", "is_admin": True})
print(user.updated_at)
---
```
# 🏠 Place

## Attributes

| Attribute | Type | Constraints |
|------------|--------|------------|
| id | String | UUID |
| title | String | Required, max 100 characters |
| description | String | Optional |
| price | Float | Must be positive |
| latitude | Float | Between -90.0 and 90.0 |
| longitude | Float | Between -180.0 and 180.0 |
| owner | User | Must be a User instance |
| reviews | List | Stores related Review objects |
| amenities | List | Stores related Amenity objects |
| created_at | DateTime | Auto-generated |
| updated_at | DateTime | Auto-updated |

## Responsibilities

- Validate geographic coordinates
- Validate positive pricing
- Maintain one-to-many relationship with `Review`
- Maintain many-to-many relationship with `Amenity`
- Reference an owning `User`

## Example Usage

```python
from app.models.user import User
from app.models.place import Place

owner = User("Alice", "Smith", "alice@example.com")

place = Place(
    title="Cozy Apartment",
    description="Nice place",
    price=100,
    latitude=37.7749,
    longitude=-122.4194,
    owner=owner
)

print(place.title)
```
# ⭐ Review

## Attributes

| Attribute | Type | Constraints |
|------------|--------|------------|
| id | String | UUID |
| text | String | Required |
| rating | Integer | Between 1 and 5 |
| place | Place | Must be a Place instance |
| user | User | Must be a User instance |
| created_at | DateTime | Auto-generated |
| updated_at | DateTime | Auto-updated |

## Responsibilities

- Validate rating range (1–5)
- Validate required text
- Maintain references to `Place` and `User`

## Example Usage

```python
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

owner = User("Alice", "Smith", "alice@example.com")
place = Place("Cozy Apartment", "Nice place", 100, 37.7749, -122.4194, owner)

review = Review(
    text="Great stay!",
    rating=5,
    place=place,
    user=owner
)

place.add_review(review)
print(len(place.reviews))  

---
```
# 🛎 Amenity

## Attributes

| Attribute | Type | Constraints |
|------------|--------|------------|
| id | String | UUID |
| name | String | Required, max 50 characters |
| created_at | DateTime | Auto-generated |
| updated_at | DateTime | Auto-updated |

## Responsibilities

- Validate that `name` is a non-empty string
- Enforce maximum length (50 characters)
- Allow association with `Place` (many-to-many simplified via list storage)

## Example Usage

```python
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity

owner = User("Alice", "Smith", "alice@example.com")
place = Place("Cozy Apartment", "Nice place", 100, 37.7749, -122.4194, owner)

wifi = Amenity("Wi-Fi")
parking = Amenity("Parking")

place.add_amenity(wifi)
place.add_amenity(parking)

print([a.name for a in place.amenities])  # ["Wi-Fi", "Parking"]
```

---

# 🌐 Presentation Layer & Facade – API Endpoints

## 📌 Overview

After implementing the Business Logic layer (Models), the second major step of Part 2 consists of exposing this logic through a RESTful API using **Flask** and **Flask-RESTx**, while ensuring clean separation of concerns.

This is achieved through:

- A **Facade layer** that centralizes all business interactions.
- A **Presentation layer (API)** that handles HTTP requests and responses.
- A structured use of **Namespaces**, **Resources**, and **Models** in Flask-RESTx.
- Consistent HTTP status codes and JSON responses.

The API does **not** interact directly with the models or repositories.  
All communication goes through the `HBnBFacade`.

---

# 🏛 HBnBFacade (Service Layer)

## 🎯 Role

The `HBnBFacade` class acts as a mediator between:

- The API (Presentation Layer)
- The Business Logic (Models)
- The Persistence Layer (Repository)

It:

- Creates entities
- Retrieves entities
- Updates entities
- Deletes reviews
- Validates relationships (User ↔ Place ↔ Review ↔ Amenity)
- Ensures data integrity before persistence

The facade holds repository instances:

- `user_repo`
- `place_repo`
- `amenity_repo`
- `review_repo`

Each repository is an instance of `InMemoryRepository`.

---

## 🔁 Why Use a Facade?

Without the facade:

- The API would directly manipulate repositories.
- Validation logic would be duplicated.
- Relations would be inconsistently handled.

With the facade:

- All coordination logic is centralized.
- The API remains clean and focused on HTTP handling.
- The persistence layer can be replaced later without changing the API.

---

# 👤 User Endpoints

## Implemented Endpoints

- `POST /api/v1/users/`
- `GET /api/v1/users/`
- `GET /api/v1/users/<user_id>`
- `PUT /api/v1/users/<user_id>`

## Responsibilities

### POST
- Validate request body via RESTx
- Check email uniqueness
- Call `facade.create_user()`
- Return `201 Created`

### GET (list)
- Call `facade.get_users()`
- Return list of serialized users

### GET (by id)
- Call `facade.get_user(user_id)`
- Return `404` if not found

### PUT
- Validate existence
- Call `facade.update_user()`
- Return updated user

---

# 🛎 Amenity Endpoints

## Implemented Endpoints

- `POST /api/v1/amenities/`
- `GET /api/v1/amenities/`
- `GET /api/v1/amenities/<amenity_id>`
- `PUT /api/v1/amenities/<amenity_id>`

## Differences Compared to User

- No uniqueness constraint required.
- Simpler entity (no direct relationship validation here).
- Used later by Place for many-to-many relationship.

---

# 🏠 Place Endpoints

## Implemented Endpoints

- `POST /api/v1/places/`
- `GET /api/v1/places/`
- `GET /api/v1/places/<place_id>`
- `PUT /api/v1/places/<place_id>`

## Special Logic for Place

Place introduces relationships:

- One-to-many: User → Places
- Many-to-many: Place ↔ Amenities
- One-to-many: Place → Reviews

### POST Place

Requires:

- owner_id (must exist)
- amenities (list of amenity IDs)

Facade responsibilities:

1. Retrieve owner via `user_repo`
2. Retrieve amenities via `amenity_repo`
3. Validate price, latitude, longitude
4. Create Place object
5. Attach amenities
6. Store in `place_repo`

Returns `201 Created`.

---

### GET Place (detail)

Returns enriched data:

- Basic fields
- Owner object (nested)
- Amenities list (nested)
- Reviews list (nested)

Requires custom serialization logic.

---

# ⭐ Review Endpoints

Review is the most complex entity in Part 2.

## Implemented Endpoints

- `POST /api/v1/reviews/`
- `GET /api/v1/reviews/`
- `GET /api/v1/reviews/<review_id>`
- `PUT /api/v1/reviews/<review_id>`
- `DELETE /api/v1/reviews/<review_id>`
- `GET /api/v1/places/<place_id>/reviews`

## Special Characteristics

- Only entity supporting DELETE.
- Must validate:
  - user_id exists
  - place_id exists
  - rating is between 1 and 5
- Must maintain bidirectional consistency:
  - Review stored in review_repo
  - Review added to place.reviews list

---

## DELETE Review Logic

1. Retrieve review
2. Remove from `review_repo`
3. Remove from associated `place.reviews`
4. Return success message

If not removed from place:
- Data becomes inconsistent.
- GET place details would still show deleted review.

---

# 🔀 Flow of Execution (End-to-End Example)

## Example: Creating a Review

1. Client sends POST /reviews/
2. RESTx validates request format.
3. API calls `facade.create_review(review_data)`.
4. Facade:
   - Retrieves User
   - Retrieves Place
   - Validates rating
   - Creates Review object
   - Stores in review_repo
   - Calls `place.add_review(review)`
5. API serializes Review object.
6. Response returned with 201.

This demonstrates full multi-layer interaction:
Presentation → Facade → Repository → Model → Repository → Presentation

---

# 🧩 Namespaces (Flask-RESTx)

Namespaces group endpoints logically:

- users
- places
- amenities
- reviews

They are registered in `create_app()` using:

api.add_namespace(namespace, path="/api/v1/...")

Purpose:

- Organize API by resource
- Structure Swagger documentation
- Prevent route collisions

---

# 📄 Swagger & Documentation

Flask-RESTx automatically generates Swagger UI:

- Documents endpoints
- Shows expected JSON body
- Displays possible response codes
- Allows interactive testing

Swagger does not contain logic.  
It reflects what is declared in:

- `api.model`
- `@api.expect`
- `@api.response`

---

# ⚠ Common Pitfalls

- Forgetting to register namespace in `create_app`
- Import errors (missing `api = Namespace(...)`)
- Not removing review from place when deleting
- Mixing 400 and 404 incorrectly
- Forgetting that in-memory repository resets on restart
- Confusing RESTx validation with business validation
- Returning inconsistent JSON structures between endpoints

---

# 📦 Final Architecture Summary

Client
↓
Flask (routing)
↓
Flask-RESTx Resource
↓
HBnBFacade
↓
Repository
↓
Model (validation + relationships)

The architecture enforces:

- Separation of concerns
- Centralized coordination
- Scalable persistence layer
- Clean API documentation
- Strong data integrity across relationships

---

This completes the Presentation Layer and Service Layer implementation of Part 2.