-- Seed data for testing
-- This creates a test user with email: test@example.com and password: admin

-- Clear existing test data (optional)
DELETE FROM acces_app WHERE email = 'test@example.com';
DELETE FROM users WHERE email = 'test@example.com';

-- Insert test user in users table
INSERT INTO users (nom, prenom, email, tel, rue, npa, localite, date_naissance)
VALUES (
    'Dupont',
    'Alice',
    'test@example.com',
    '+41 79 123 45 67',
    'Rue de la Gare 15',
    '1920',
    'Martigny',
    '1990-01-15'
);

-- Insert credentials in acces_app table
-- Password hash for "admin" generated with bcrypt
-- You can generate a new hash with: python -c "from passlib.hash import bcrypt; print(bcrypt.hash('admin'))"
INSERT INTO acces_app (email, password_hash)
VALUES (
    'test@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYtPZJqU6F6'
);

-- Verify the data was inserted
SELECT * FROM users WHERE email = 'test@example.com';
SELECT email FROM acces_app WHERE email = 'test@example.com';
