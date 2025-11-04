-- Seed data for testing
-- This creates a test user with email: test@example.com and password: admin

-- Insert test user in users table
INSERT INTO users (user_nom, user_prenom, user_email, user_telephone, user_rue, user_npa, user_localite, user_date_naissance)
VALUES (
    'Dupont',
    'Alice',
    'test@example.com',
    '+41 79 123 45 67',
    'Rue de la Gare 15',
    '1920',
    'Martigny',
    '1990-01-15'
)
ON DUPLICATE KEY UPDATE user_nom=user_nom;

-- Insert credentials in acces_app table
-- Password hash for "admin" generated with bcrypt
INSERT INTO acces_app (user_email, acces_password)
VALUES (
    'test@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYtPZJqU6F6'
)
ON DUPLICATE KEY UPDATE acces_password=VALUES(acces_password);

-- Verify the data was inserted
SELECT user_email, user_nom, user_prenom FROM users WHERE user_email = 'test@example.com';
SELECT user_email FROM acces_app WHERE user_email = 'test@example.com';
