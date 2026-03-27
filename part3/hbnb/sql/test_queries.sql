-- =========================================================
-- TEST QUERIES FOR HBnB DATABASE
-- =========================================================

-- =========================================================
-- 1. VERIFY INITIAL DATA
-- =========================================================

-- Check admin user
SELECT id, first_name, last_name, email, is_admin
FROM users
WHERE email = 'admin@hbnb.io';

-- Check initial amenities
SELECT id, name
FROM amenities;

-- =========================================================
-- 2. CREATE TEST USERS
-- =========================================================

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Alice',
    'Tester',
    'alice@example.com',
    'hashed_password_here',
    FALSE
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'Bob',
    'Reviewer',
    'bob@example.com',
    'hashed_password_here',
    FALSE
);

-- Verify users
SELECT * FROM users
WHERE email IN ('alice@example.com', 'bob@example.com');

-- =========================================================
-- 3. CREATE A TEST PLACE
-- =========================================================

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    'Test Place',
    'A place for SQL testing',
    120.00,
    48.8566,
    2.3522,
    '11111111-1111-1111-1111-111111111111'
);

-- Verify place
SELECT * FROM places
WHERE id = '33333333-3333-3333-3333-333333333333';

-- =========================================================
-- 4. LINK PLACE TO AMENITIES
-- =========================================================

-- Use IDs from seed.sql
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    '4b1c33dd-aec2-4c8b-a703-2b621dd0709f'
);

INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    'b3f72daf-736a-4340-931e-aee96c05c8a8'
);

-- Verify place_amenity links
SELECT * FROM place_amenity
WHERE place_id = '33333333-3333-3333-3333-333333333333';

-- =========================================================
-- 5. CREATE A REVIEW
-- =========================================================

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    'Excellent stay',
    5,
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333'
);

-- Verify review
SELECT * FROM reviews
WHERE id = '44444444-4444-4444-4444-444444444444';

-- =========================================================
-- 6. READ RELATIONS WITH JOINS
-- =========================================================

-- Show place with owner
SELECT
    p.id AS place_id,
    p.title,
    u.id AS owner_id,
    u.first_name,
    u.last_name,
    u.email
FROM places p
JOIN users u ON p.owner_id = u.id
WHERE p.id = '33333333-3333-3333-3333-333333333333';

-- Show reviews with reviewer and place
SELECT
    r.id AS review_id,
    r.text,
    r.rating,
    u.email AS reviewer_email,
    p.title AS place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
WHERE r.id = '44444444-4444-4444-4444-444444444444';

-- Show amenities of a place
SELECT
    p.title,
    a.name AS amenity_name
FROM place_amenity pa
JOIN places p ON pa.place_id = p.id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = '33333333-3333-3333-3333-333333333333';

-- =========================================================
-- 7. UPDATE TESTS
-- =========================================================

-- Update user first name
UPDATE users
SET first_name = 'Alicia'
WHERE id = '11111111-1111-1111-1111-111111111111';

SELECT * FROM users
WHERE id = '11111111-1111-1111-1111-111111111111';

-- Update place price
UPDATE places
SET price = 150.00
WHERE id = '33333333-3333-3333-3333-333333333333';

SELECT * FROM places
WHERE id = '33333333-3333-3333-3333-333333333333';

-- Update review text
UPDATE reviews
SET text = 'Amazing stay with great comfort'
WHERE id = '44444444-4444-4444-4444-444444444444';

SELECT * FROM reviews
WHERE id = '44444444-4444-4444-4444-444444444444';

-- =========================================================
-- 8. DELETE TESTS
-- =========================================================

-- Delete one place_amenity link
DELETE FROM place_amenity
WHERE place_id = '33333333-3333-3333-3333-333333333333'
  AND amenity_id = 'b3f72daf-736a-4340-931e-aee96c05c8a8';

SELECT * FROM place_amenity
WHERE place_id = '33333333-3333-3333-3333-333333333333';

-- =========================================================
-- 9. INTEGRITY TESTS (RUN ONE BY ONE)
-- =========================================================

-- 9.1 Duplicate email -> should fail
-- INSERT INTO users (id, first_name, last_name, email, password, is_admin)
-- VALUES (
--     '55555555-5555-5555-5555-555555555555',
--     'Duplicate',
--     'Email',
--     'alice@example.com',
--     'hash',
--     FALSE
-- );

-- 9.2 Invalid rating -> should fail
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES (
--     '66666666-6666-6666-6666-666666666666',
--     'Invalid rating test',
--     8,
--     '22222222-2222-2222-2222-222222222222',
--     '33333333-3333-3333-3333-333333333333'
-- );

-- 9.3 Duplicate review for same user/place -> should fail
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES (
--     '77777777-7777-7777-7777-777777777777',
--     'Second review same place',
--     4,
--     '22222222-2222-2222-2222-222222222222',
--     '33333333-3333-3333-3333-333333333333'
-- );

-- 9.4 Duplicate place_amenity link -> should fail
-- INSERT INTO place_amenity (place_id, amenity_id)
-- VALUES (
--     '33333333-3333-3333-3333-333333333333',
--     '4b1c33dd-aec2-4c8b-a703-2b621dd0709f'
-- );

-- =========================================================
-- 10. CLEANUP TEST DATA
-- =========================================================

DELETE FROM reviews
WHERE id = '44444444-4444-4444-4444-444444444444';

DELETE FROM place_amenity
WHERE place_id = '33333333-3333-3333-3333-333333333333';

DELETE FROM places
WHERE id = '33333333-3333-3333-3333-333333333333';

DELETE FROM users
WHERE id IN (
    '11111111-1111-1111-1111-111111111111',
    '22222222-2222-2222-2222-222222222222'
);

-- Final verification
SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM place_amenity;
SELECT * FROM amenities;