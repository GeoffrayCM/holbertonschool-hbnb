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