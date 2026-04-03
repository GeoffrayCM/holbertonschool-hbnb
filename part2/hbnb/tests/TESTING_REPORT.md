# HBnB – Part 2  
# Testing Report (Short Version)

## 1. Overview

This document summarizes the testing process implemented for the HBnB API (Part 2).

Testing was performed using:

- Automated unit tests (unittest)
- Manual testing with cURL
- Swagger documentation (Flask-RESTx)

Persistence layer: In-memory repositories

Test command used:

python3 -m unittest discover -s tests -p "test_*.py" -v

---

## 2. Automated Unit Tests Coverage

Four main test modules were implemented:

- test_users.py
- test_amenities.py
- test_places.py
- test_reviews.py

Each module validates both positive and negative scenarios.

---

## 3. Users Endpoints

Tested Endpoints:

- POST /api/v1/users/
- GET /api/v1/users/<user_id>

Test Cases:

✔ Create valid user  
Input:
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}
Expected: 201 Created  
Result: PASS

✔ Duplicate email  
Expected: 400 Bad Request  
Result: PASS

✔ Invalid email format  
Expected: 400 Bad Request  
Result: PASS

✔ Get non-existent user  
Expected: 404 Not Found  
Result: PASS

---

## 4. Amenities Endpoints

Tested Endpoints:

- POST /api/v1/amenities/
- GET /api/v1/amenities/
- GET /api/v1/amenities/<amenity_id>

Test Cases:

✔ Create valid amenity  
Expected: 201  
Result: PASS

✔ Invalid name (empty string)  
Expected: 400  
Result: PASS

✔ Retrieve amenities list  
Expected: 200  
Result: PASS

✔ Get non-existent amenity  
Expected: 404  
Result: PASS

---

## 5. Places Endpoints

Tested Endpoints:

- POST /api/v1/places/
- GET /api/v1/places/<place_id>

Test Cases:

✔ Create valid place  
Expected: 201  
Result: PASS

✔ Invalid latitude (> 90)  
Expected: 400  
Result: PASS

✔ Invalid owner_id  
Expected: 400  
Result: PASS

✔ Retrieve place details  
Expected:
- 200
- Includes nested owner
- Includes amenities list  
Result: PASS

---

## 6. Reviews Endpoints

Tested Endpoints:

- POST /api/v1/reviews/
- GET /api/v1/reviews/
- GET /api/v1/reviews/<review_id>
- GET /api/v1/places/<place_id>/reviews
- DELETE /api/v1/reviews/<review_id>

Test Cases:

✔ Create valid review  
Expected: 201  
Result: PASS

✔ Invalid rating (>5)  
Expected: 400  
Result: PASS

✔ Retrieve reviews by place  
Expected: 200 + list containing review  
Result: PASS

✔ Delete review  
Expected: 200  
Result: PASS

✔ Verify review removed from place after deletion  
Expected: Review not present in place reviews list  
Result: PASS

---

## 7. Issues Encountered and Fixes

Issue 1: 500 Internal Server Error on invalid data  
Cause:
Model raised ValueError but endpoint did not handle it.

Fix:
Added try/except (ValueError, TypeError) in API endpoints to return 400.

Issue 2: Review creation failing  
Cause:
Typo in facade ("ating" instead of "rating").

Fix:
Corrected parameter name in create_review.

---

## 8. Conclusion

All endpoints were validated through:

- Model-level validation
- Facade logic validation
- API response validation
- Automated unit testing
- Relationship integrity checks (Place ↔ Amenities, Place ↔ Reviews)

All implemented unit tests pass successfully.

The API correctly handles:

- Valid input
- Invalid input
- Missing resources
- Relationship consistency
- Proper HTTP status codes