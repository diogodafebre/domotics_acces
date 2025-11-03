# Move Acces - Full Stack Application

Complete full-stack application with Flutter mobile app, FastAPI backend, MySQL database, Redis cache, and Caddy reverse proxy.

## 🎯 Overview

**Move Acces** is a production-ready mobile application with a scalable backend infrastructure designed to handle ~2,700 users/day with peak concurrent loads.

### Tech Stack

- **Mobile**: Flutter 3.16+ (Android & iOS)
- **Backend**: FastAPI (Python 3.11+) with async SQLAlchemy
- **Database**: MySQL 8.0 (existing schema)
- **Cache/Sessions**: Redis 7
- **Reverse Proxy**: Caddy 2 (automatic HTTPS)
- **Infrastructure**: Docker Compose
- **CI/CD**: GitHub Actions

## 📋 Features

### Mobile App
- JWT authentication with automatic token refresh
- Secure token storage (flutter_secure_storage)
- User profile management
- Real-time communication (WebSocket)
- Offline support (Drift/SQLite)
- Material Design 3
- State management with Riverpod
- Navigation with go_router

### Backend API
- RESTful API with OpenAPI/Swagger docs
- JWT authentication (access + refresh tokens)
- Argon2id password hashing
- Rate limiting (Redis-based)
- CORS protection
- Audit logging
- WebSocket support
- Prometheus metrics
- Connection pooling (MySQL)
- Async/await throughout

### Security
- TLS/HTTPS everywhere (Caddy automatic certificates)
- Secure password hashing (Argon2id)
- JWT tokens with short TTL
- Refresh token blacklisting
- Rate limiting (login: 5/min, API: 100/5min)
- SQL injection protection (prepared statements)
- No database exposure to internet
- Security headers (HSTS, CSP, etc.)

## 🏗️ Architecture

```
┌─────────────────┐
│  Flutter App    │ (Mobile - Android/iOS)
│  (Riverpod)     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Caddy Proxy    │ (TLS termination, reverse proxy)
│  (Port 443)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────┐
│  FastAPI API    │────▶│   Redis     │ (Sessions, cache, rate-limit)
│  (Port 8000)    │     └─────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MySQL 8.0      │ (Existing schema - DO NOT MODIFY)
│  (Internal)     │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Flutter SDK 3.16+ (for mobile development)
- Git

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Domotics-Acces.git
cd Domotics-Acces
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important variables:**
- `APP_SECRET`: 32+ character secret key (generate with `openssl rand -hex 32`)
- `DB_PASSWORD`: Secure database password
- `DB_ROOT_PASSWORD`: MySQL root password

### 3. Start Services

```bash
# Start all services (dev mode)
make up-build

# Or manually:
docker compose -f deploy/docker-compose.dev.yml up --build -d
```

### 4. Initialize Database

```bash
# Run migrations (only for new tables)
make migrate

# Seed test data
make seed
```

Test credentials after seeding:
- Email: `diogofebre@gmail.com`
- Password: `TestPassword123!`

### 5. Run Mobile App

```bash
cd mobile
flutter pub get
flutter run --dart-define=API_BASE_URL=http://localhost:8080
```

For Android emulator, use `http://10.0.2.2:8080` instead of `localhost`.

## 📁 Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/      # SQLAlchemy models (existing schema)
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── routers/     # API endpoints
│   │   ├── security/    # Auth, passwords, tokens
│   │   └── utils/       # Rate limit, audit, logging
│   ├── alembic/         # Database migrations (new tables only)
│   ├── tests/           # Pytest tests
│   └── Dockerfile
│
├── mobile/              # Flutter mobile app
│   ├── lib/
│   │   ├── core/        # Network, config
│   │   ├── features/    # Auth, profile, dashboard, settings
│   │   ├── services/    # WebSocket
│   │   └── main.dart
│   ├── integration_test/
│   └── test/
│
├── deploy/              # Infrastructure
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── Caddyfile.dev
│   ├── Caddyfile.prod
│   └── init.sql         # Schema initialization
│
├── ops/                 # Operations scripts
│   └── scripts/
│       ├── seed.py
│       └── migrate.sh
│
├── .github/
│   └── workflows/
│       └── ci.yml       # CI/CD pipeline
│
├── Makefile             # Common commands
└── README.md
```

## 🗄️ Database Schema (Existing - DO NOT MODIFY)

The MySQL database contains three existing tables that **must not be altered**:

### `users`
- `user_id` (PK, auto-increment)
- `email` (unique)
- `nom`, `prenom`, `date_naissance`
- `rue`, `npa`, `localite`, `tel`
- `created_at`, `updated_at`

### `acces_app`
- `email` (PK, FK to users)
- `password_hash` (Argon2id)

### `abonnement`
- `abo_id` (PK, auto-increment)
- `user_id` (FK to users)
- `abo_state` (enum: active, paused, expired, canceled, pending)
- `abo_name`, `abo_date_start`, `abo_date_stop`
- `abo_price`, `abo_discount`, etc.

### New Tables (Created by Alembic)

- `audit_logs`: Security audit trail

## 🔑 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns access + refresh tokens)
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout (blacklist refresh token)

### Users
- `GET /users/me` - Get current user profile
- `PATCH /users/me` - Update profile

### WebSocket
- `GET /ws?token={access_token}` - WebSocket connection

### Monitoring
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Swagger UI (dev only)

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
make test-backend

# Or in backend directory:
cd backend
poetry run pytest -v

# With coverage
poetry run pytest --cov=app --cov-report=html
```

### Mobile Tests

```bash
# Unit & widget tests
make test-mobile

# Or in mobile directory:
cd mobile
flutter test

# Integration tests (requires running backend)
flutter test integration_test/auth_flow_test.dart
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Install dependencies
poetry install

# Run locally (requires MySQL & Redis)
uvicorn app.main:app --reload

# Lint
ruff check .
black --check .
isort --check-only .

# Format
black .
isort .
```

### Mobile Development

```bash
cd mobile

# Get dependencies
flutter pub get

# Analyze
flutter analyze

# Format
dart format .

# Run on device
flutter devices
flutter run --dart-define=API_BASE_URL=http://localhost:8080
```

## 📦 Deployment

### Production Deployment

1. **Configure production environment:**

```bash
cp .env.example .env
# Set production values:
# - Strong APP_SECRET
# - Production DB_URL (external MySQL)
# - CADDY_DOMAIN (your domain)
# - CADDY_EMAIL (for Let's Encrypt)
```

2. **Deploy with Docker Compose:**

```bash
make prod-up

# Or manually:
docker compose -f deploy/docker-compose.prod.yml up -d
```

3. **Build mobile apps:**

```bash
# Android
cd mobile
flutter build apk --release --dart-define=API_BASE_URL=https://api.yourdomain.com

# iOS
flutter build ios --release --dart-define=API_BASE_URL=https://api.yourdomain.com
```

### Important Production Considerations

- Use external managed MySQL (not in container)
- Configure proper backup strategy
- Set up monitoring (Prometheus + Grafana)
- Configure log aggregation
- Use secrets management (not .env files)
- Set up SSL certificate renewal monitoring
- Configure firewall rules (only 80/443 exposed)
- Enable MySQL SSL/TLS connections
- Regular security updates

## 🔍 Monitoring & Observability

### Metrics

Prometheus metrics available at `/metrics`:
- Request counts and latencies
- Error rates
- Active connections
- Custom business metrics

### Logs

Structured JSON logging to stdout:
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "message": "User logged in",
  "user_id": 123,
  "ip": "192.168.1.1"
}
```

### Health Checks

- API: `GET /health`
- MySQL: Connection pool health
- Redis: Ping command

## 🛡️ Security Best Practices

### Implemented
- ✅ Argon2id password hashing (memory: 64MB, iterations: 3)
- ✅ JWT with short TTL (access: 15min, refresh: 24h)
- ✅ Refresh token blacklisting (Redis)
- ✅ Rate limiting (login & API)
- ✅ CORS strict origin checking
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ XSS protection headers
- ✅ HTTPS/TLS everywhere
- ✅ Audit logging
- ✅ No database port exposure

### Recommendations
- 🔒 Use hardware security modules (HSM) for production secrets
- 🔒 Implement 2FA for sensitive operations
- 🔒 Regular security audits
- 🔒 Penetration testing before production
- 🔒 DDoS protection (Cloudflare, AWS Shield)
- 🔒 WAF (Web Application Firewall)

## 📊 Performance

### Target Metrics
- ~2,700 users/day
- Peak concurrent users: 500+
- API p95 latency: <200ms
- WebSocket concurrent connections: 1,000+

### Optimization
- Connection pooling (MySQL: 20 + 20 overflow)
- Redis caching
- Async I/O throughout
- Indexed database queries
- Rate limiting to prevent abuse

### Scaling
- Backend: Horizontal scaling (stateless)
- Database: Read replicas, connection pooling
- Redis: Redis Cluster or Sentinel
- Load balancing: Multiple Caddy instances

## 🐛 Troubleshooting

### Backend Issues

**Can't connect to MySQL:**
- Check `DB_URL` in environment
- Verify MySQL container is running: `docker ps`
- Check logs: `docker logs move-acces-mysql`

**Redis connection errors:**
- Verify Redis container: `docker ps | grep redis`
- Check Redis logs: `docker logs move-acces-redis`

**Migration errors:**
- Don't modify existing tables
- Check Alembic history: `alembic current`
- Review migration logs

### Mobile Issues

**Can't connect to API:**
- Android emulator: Use `10.0.2.2` instead of `localhost`
- iOS simulator: Use `localhost` is fine
- Check API_BASE_URL configuration
- Verify backend is running: `curl http://localhost:8080/health`

**Token refresh not working:**
- Clear app data and re-login
- Check backend logs for token validation errors
- Verify APP_SECRET matches between backend instances

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit pull request

## 📝 Assumptions & Adaptations

### Database Schema
- Existing schema is production and must not be altered
- NPA field is always 4 digits (Swiss postal codes)
- Phone numbers stored as strings (international format support)
- Email is unique identifier across tables

### Authentication
- No MQTT used (requirement: HTTP/HTTPS only)
- Tokens stored client-side (secure storage)
- Single device login (can be extended to multi-device)

### Scaling
- Backend is stateless (can scale horizontally)
- WebSocket connections handled in-memory (can move to Redis pub/sub)
- File uploads not implemented (add S3/MinIO if needed)

## 📄 License

© 2024 Move Acces. All rights reserved.

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/Domotics-Acces/issues)
- Email: support@yourdomain.com

---

**Built with ❤️ using Flutter, FastAPI, and Docker**
