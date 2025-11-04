# Domotics Access API - Backend FastAPI

API d'authentification JWT pour l'application mobile Domotics.

## Technologies

- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM pour MySQL
- **JWT (python-jose)** - Authentification par tokens
- **Bcrypt (passlib)** - Hachage sécurisé des mots de passe
- **MySQL** - Base de données existante `move_acces`

## Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py         # Endpoints /auth/login, /auth/refresh, /me
│   │   └── users.py        # Endpoints utilisateurs (expansion future)
│   ├── core/
│   │   ├── config.py       # Configuration via variables d'env
│   │   └── security.py     # JWT et bcrypt
│   ├── db/
│   │   ├── models.py       # Modèles SQLAlchemy (users, acces_app, abonnement)
│   │   └── session.py      # Connexion DB avec pooling
│   └── schemas/
│       ├── auth.py         # Schémas Pydantic pour auth
│       └── user.py         # Schémas Pydantic pour users
├── Dockerfile
├── requirements.txt
├── .env.example
└── seed.sql               # Données de test
```

## Installation et lancement

### 1. Prérequis

- Python 3.11+
- MySQL avec base de données `move_acces` existante
- Tables : `users`, `acces_app`, `abonnement`

### 2. Configuration

Copier `.env.example` vers `.env` et adapter les valeurs :

```bash
cp .env.example .env
```

Éditer `.env` avec vos paramètres MySQL :

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=move_acces
DB_USER=root
DB_PASS=votre_mot_de_passe
JWT_SECRET=changez_moi_en_production
JWT_ALG=HS256
ACCESS_EXPIRE_MIN=15
REFRESH_EXPIRE_DAYS=15
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer un utilisateur de test

Importer le fichier `seed.sql` dans votre base MySQL :

```bash
mysql -u root -p move_acces < seed.sql
```

Cela crée un utilisateur de test :
- **Email** : `test@example.com`
- **Mot de passe** : `admin`

### 5. Lancer le serveur

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera accessible sur `http://localhost:8000`

Documentation auto-générée : `http://localhost:8000/docs`

## Endpoints

### POST /auth/login

Authentification avec email et mot de passe.

**Request:**
```json
{
  "email": "test@example.com",
  "password": "admin"
}
```

**Response (200):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "test@example.com",
    "prenom": "Alice",
    "nom": "Dupont"
  }
}
```

**Response (401):**
```json
{
  "detail": "Invalid credentials"
}
```

### POST /auth/refresh

Rafraîchir le token d'accès.

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

### GET /auth/me

Récupérer les informations de l'utilisateur connecté.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "test@example.com",
  "prenom": "Alice",
  "nom": "Dupont"
}
```

**Response (401):**
```json
{
  "detail": "Invalid or expired token"
}
```

## Exemples cURL

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"admin"}'
```

### Get current user
```bash
# Remplacer <ACCESS_TOKEN> par le token reçu lors du login
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Refresh token
```bash
# Remplacer <REFRESH_TOKEN> par le refresh token reçu lors du login
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<REFRESH_TOKEN>"}'
```

## Docker

### Build
```bash
docker build -t domotics-api .
```

### Run
```bash
docker run -p 8000:8000 --env-file .env domotics-api
```

## Sécurité

- Les mots de passe sont hachés avec **bcrypt** (jamais stockés en clair)
- Les tokens JWT sont signés avec **HS256**
- CORS activé (configurer `CORS_ORIGINS` pour la production)
- Access token expire après 15 minutes
- Refresh token expire après 15 jours

## Générer un hash bcrypt

Pour créer un nouvel utilisateur, générer le hash bcrypt du mot de passe :

```python
python -c "from passlib.hash import bcrypt; print(bcrypt.hash('votre_mot_de_passe'))"
```

Puis insérer dans la base :

```sql
INSERT INTO acces_app (email, password_hash)
VALUES ('nouveau@example.com', '$2b$12$...');

INSERT INTO users (email, nom, prenom)
VALUES ('nouveau@example.com', 'Nom', 'Prenom');
```

## Support

Documentation FastAPI : https://fastapi.tiangolo.com/
