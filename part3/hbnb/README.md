# 🧱 HBnB — Part 3: Persistence & Authentication

---

# 📌 Overview

Part 3 of the HBnB project represents the transition from a conceptual and in-memory application to a **fully persistent and secured backend system**.

In this phase, the project integrates:

- A real relational database via **SQLAlchemy**
- Secure authentication using **JWT (JSON Web Tokens)**
- Advanced relationship management between entities
- Enforcement of business rules at both application and database levels

This part completes the backend foundation, making the API **robust, consistent, and production-ready**.

---

# 🏗️ Architecture Evolution

The layered architecture introduced in Part 2 is preserved and enhanced:

```
Presentation Layer (Flask / Flask-RESTx API)
        ↓
Business Logic Layer (Facade + Models)
        ↓
Persistence Layer (SQLAlchemy Repositories + Database)
```

### Key Improvements

- In-memory storage → replaced by **database persistence**
- Open endpoints → secured with **JWT authentication**
- Basic entities → enriched with **real relationships**

---

# 🗄️ Database Integration (SQLAlchemy)

## ORM Mapping

Each business entity is mapped to a database table:

| Entity   | Table       |
|----------|------------|
| User     | users      |
| Place    | places     |
| Review   | reviews    |
| Amenity  | amenities  |

---

## Relationships Implemented

### 🔹 User ↔ Place
- One-to-Many
- A user can own multiple places

```python
user_id = db.Column(db.String(36), db.ForeignKey("users.id"))
owner = db.relationship("User", backref="places")
```

---

### 🔹 User ↔ Review
- One-to-Many
- A user can write multiple reviews

---

### 🔹 Place ↔ Review
- One-to-Many
- A place can have multiple reviews

---

### 🔹 Place ↔ Amenity
- Many-to-Many
- Implemented via association table:

```python
place_amenity = db.Table(...)
```

---

## Key Concepts Introduced

- `db.Column`, `db.ForeignKey`
- `db.relationship`
- Association tables (Many-to-Many)
- Lazy loading strategies
- ORM ↔ SQL abstraction

---

# 🔐 Authentication (JWT)

## Implementation

Authentication is handled using:

- `flask-jwt-extended`

## Features

- Login endpoint (`/auth/login`)
- JWT token generation
- Token-based request protection
- Role-based access control

---

## Roles

### 👑 Admin
- Can create users
- Has full privileges

### 👤 Normal User
- Can update own profile (restricted fields)
- Can create places
- Can create reviews (with rules)

---

## Protected Endpoints

Example:

```python
@jwt_required()
def post(self):
```

---

# 🧠 Business Rules Enforced

## Application-Level Rules

- A user cannot review their own place
- A user cannot review the same place twice
- Only admin can create users
- Users cannot modify restricted fields

---

## Database-Level Constraints

- `email` is UNIQUE
- `(user_id, place_id)` UNIQUE in reviews
- Rating must be between 1 and 5
- Foreign key constraints ensure integrity

---

# 🧾 SQL Scripts (Understanding the Database)

Even though SQLAlchemy manages the database, raw SQL scripts were created to:

- Reproduce the schema manually
- Understand ORM internals
- Validate constraints independently

## Files

- `schema.sql` → table creation
- `seed.sql` → initial data
- `test_queries.sql` → manual testing

---

# 🧪 Testing Strategy

## 1. Automated Script

- `test_relations.py`
- Validates:
  - entity creation
  - relationships
  - constraints

---

## 2. Swagger Testing

- Interactive API testing
- JWT token integration
- Quick validation of endpoints

---

## 3. cURL Testing

- Full manual control
- Useful for debugging and scripting

---

## Tested Features

- Authentication flow
- CRUD operations
- Relationship consistency
- Constraint enforcement

---

# 🔁 End-to-End Flow Example

1. Admin logs in → gets token
2. Admin creates users
3. Users log in
4. User creates a place
5. Amenities are linked
6. Another user creates a review
7. API returns:
   - place with owner
   - amenities
   - reviews

---

# 🧩 Design Patterns Used

## Repository Pattern
- Abstracts database access
- Clean separation of persistence logic

## Facade Pattern
- Central entry point for business logic
- Simplifies API layer interactions

---

# 🚀 What Part 3 Achieves

- Real database persistence
- Secure authentication system
- Full relationship modeling
- Strong data integrity guarantees
- Production-ready API foundation

---

# 📊 Summary

| Feature                  | Status |
|-------------------------|--------|
| SQLAlchemy integration  | ✅ |
| JWT authentication      | ✅ |
| Role management         | ✅ |
| Relationships           | ✅ |
| Business rules          | ✅ |
| SQL schema scripts      | ✅ |
| API testing             | ✅ |

---

# 🎯 Conclusion

Part 3 transforms HBnB into a **complete backend system**:

- Structured
- Secure
- Scalable
- Maintainable

It bridges the gap between **architecture (Part 1 & 2)** and **real-world backend implementation**, preparing the project for further extensions such as frontend integration or deployment.

---