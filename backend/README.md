# Move Acces Backend

FastAPI backend for Move Acces mobile application.

## Features

- **Authentication**: JWT-based auth with refresh tokens
- **Password Hashing**: Argon2id for secure password storage
- **Rate Limiting**: Redis-based rate limiting for login and API endpoints
- **WebSocket**: Real-time communication support
- **Audit Logging**: Track user actions for security
- **Observability**: Prometheus metrics at `/metrics`
- **Database**: MySQL with async SQLAlchemy
- **Migrations**: Alembic for database schema management

## Requirements

- Python 3.11+
- MySQL 8.0+
- Redis 6.0+

## Installation

```bash
# Install with Poetry
poetry install

# Or with pip
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure:

```env
DB_URL=mysql+asyncmy://user:password@localhost:3306/move_acces
REDIS_URL=redis://localhost:6379/0
APP_SECRET=your_secret_key_here
ACCESS_TOKEN_TTL_MIN=15
REFRESH_TOKEN_TTL_HOURS=24
```

## Database Setup

```bash
# Run migrations (only for new tables, not existing schema)
alembic upgrade head

# Seed test data
python ops/scripts/seed.py
```

## Running

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with email/password
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout and invalidate refresh token

### Users

- `GET /users/me` - Get current user profile
- `PATCH /users/me` - Update current user profile

### WebSocket

- `GET /ws?token=<access_token>` - WebSocket connection

## Database Schema

The backend uses existing MySQL tables:

- `users` - User accounts
- `acces_app` - Login credentials
- `abonnement` - Subscriptions
- `audit_logs` - Audit trail (new table)

**Important**: Do NOT modify existing tables. Alembic is only for new tables.

## Rate Limits

- Login: 5 requests/minute per IP
- API: 100 requests/5 minutes per IP

## Security

- Argon2id password hashing
- JWT tokens (HS256)
- CORS configuration
- Rate limiting
- Audit logging
- No database exposure

## Linting & Formatting

```bash
# Check code
ruff check .
black --check .
isort --check-only .

# Format code
black .
isort .
```
