# Domotics Access - V1 Opérationnelle

Système complet d'authentification avec **Backend FastAPI** + **App Flutter Mobile** utilisant JWT et base de données MySQL existante.

## Vue d'ensemble

- **Backend** : API REST FastAPI avec authentification JWT (bcrypt + HS256)
- **App Mobile** : Application Flutter (Android/iOS) avec login et dashboard
- **Base de données** : MySQL existante `move_acces` (tables : users, acces_app, abonnement)

## Structure du projet

```
Domotics-Acces/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/          # Endpoints (auth, users)
│   │   ├── core/         # Config, security
│   │   ├── db/           # Models, session
│   │   └── schemas/      # Pydantic schemas
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── seed.sql          # Données de test
│   └── README.md
│
└── app/                  # Application Flutter
    ├── lib/
    │   ├── main.dart
    │   ├── models/       # User model
    │   ├── pages/        # Login, Dashboard
    │   ├── services/     # API client
    │   └── state/        # Auth state management
    ├── pubspec.yaml
    └── README.md
```

## Quick Start (< 15 min)

### 1. Backend FastAPI

```bash
cd backend

# Configuration
cp .env.example .env
# Éditer .env avec vos paramètres MySQL

# Installation
pip install -r requirements.txt

# Créer un utilisateur de test
mysql -u root -p move_acces < seed.sql

# Lancer le serveur
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Le backend est accessible sur `http://localhost:8000`

Documentation API : `http://localhost:8000/docs`

### 2. App Flutter

```bash
cd app

# Installation des dépendances
flutter pub get

# Lancer l'app (émulateur ou device)
flutter run --dart-define=API_BASE_URL=http://localhost:8000

# Sur device physique Android/iOS, remplacer localhost par l'IP de votre machine
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000
```

### 3. Test

**Identifiants de test** :
- Email : `test@example.com`
- Mot de passe : `admin`

**Flux de test** :
1. Ouvrir l'app Flutter
2. Saisir les identifiants de test
3. Cliquer sur "Se connecter"
4. Dashboard s'affiche avec les informations utilisateur
5. Pull-to-refresh pour mettre à jour les données
6. Bouton "Se déconnecter" pour retourner au login

## Fonctionnalités implémentées

### Backend (FastAPI)

- ✅ POST /auth/login - Authentification avec email/password (bcrypt)
- ✅ POST /auth/refresh - Rafraîchissement du access token
- ✅ GET /auth/me - Récupération du profil utilisateur (protégé)
- ✅ Middleware CORS activé
- ✅ JWT avec access (15 min) et refresh (15 jours)
- ✅ SQLAlchemy ORM avec pooling MySQL
- ✅ Gestion des erreurs (401, validation)
- ✅ Docker ready

### App Flutter

- ✅ Page de login avec validation (email, password)
- ✅ Stockage sécurisé des tokens JWT (flutter_secure_storage)
- ✅ Intercepteur Dio pour Authorization header automatique
- ✅ Refresh automatique du access token sur 401
- ✅ Dashboard avec affichage du profil (GET /auth/me)
- ✅ Pull-to-refresh
- ✅ Logout avec confirmation
- ✅ Gestion des états (loading, erreurs)
- ✅ Material Design 3

## Architecture

### Authentification JWT

1. **Login** : POST /auth/login
   - Vérification email dans `acces_app`
   - Vérification bcrypt du password
   - Récupération du profil depuis `users`
   - Génération des tokens JWT (access + refresh)

2. **Requêtes protégées** : Authorization: Bearer <access>
   - Validation du token
   - Extraction du user_id
   - Vérification dans la DB

3. **Refresh** : POST /auth/refresh
   - Validation du refresh token
   - Génération d'un nouveau access token

4. **App Flutter**
   - Intercepteur Dio ajoute le Bearer token
   - Sur 401 : tentative de refresh automatique
   - Si refresh OK : retry de la requête
   - Si refresh KO : logout + retour login

### Base de données (existante - non modifiée)

**Tables** :
- `users` : Profils utilisateurs (user_id, nom, prenom, email, etc.)
- `acces_app` : Credentials d'accès (email PK, password_hash bcrypt)
- `abonnement` : Abonnements liés aux users (abo_id, user_id FK, etc.)

**Liens** :
- `acces_app.email` ↔ `users.email`
- `abonnement.user_id` ↔ `users.user_id`

## Critères d'acceptation

- ✅ Build OK des 2 parties (backend + Flutter)
- ✅ POST /auth/login retourne access + refresh + user info
- ✅ GET /auth/me refuse sans Bearer et fonctionne avec Bearer
- ✅ Flutter stocke les tokens et gère le refresh automatique
- ✅ UX propre avec states (loading, erreurs), messages clairs
- ✅ Aucune modification du schéma MySQL
- ✅ README détaillés pour lancement rapide

## Sécurité

- Mots de passe **jamais stockés en clair** (bcrypt)
- Tokens JWT signés (HS256)
- Stockage sécurisé des tokens sur mobile (Keychain/Keystore)
- CORS configuré (à restreindre en prod)
- Access token court (15 min) pour limiter l'exposition
- Refresh token long (15 jours) pour UX fluide

## Génération de hash bcrypt

Pour créer de nouveaux utilisateurs :

```python
python -c "from passlib.hash import bcrypt; print(bcrypt.hash('votre_mdp'))"
```

Puis insérer dans MySQL :

```sql
INSERT INTO acces_app (email, password_hash)
VALUES ('new@example.com', '$2b$12$...');

INSERT INTO users (email, nom, prenom)
VALUES ('new@example.com', 'Nom', 'Prenom');
```

## Endpoints API

### POST /auth/login
Request :
```json
{"email": "test@example.com", "password": "admin"}
```

Response :
```json
{
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc...",
  "user": {"id": 1, "email": "test@example.com", "prenom": "Alice", "nom": "Dupont"}
}
```

### POST /auth/refresh
Request :
```json
{"refresh": "eyJhbGc..."}
```

Response :
```json
{"access": "eyJhbGc..."}
```

### GET /auth/me
Headers : `Authorization: Bearer <access>`

Response :
```json
{"id": 1, "email": "test@example.com", "prenom": "Alice", "nom": "Dupont"}
```

## Troubleshooting

### Backend ne démarre pas
- Vérifier les paramètres MySQL dans .env
- Vérifier que MySQL est lancé et accessible
- Vérifier que les dépendances sont installées

### App Flutter ne se connecte pas
- Vérifier que le backend est lancé
- Utiliser l'IP réseau (pas localhost) sur device physique
- Pour émulateur Android : `10.0.2.2:8000`
- Vérifier les logs du backend et de l'app

### "Invalid credentials"
- Vérifier que seed.sql a été importé
- Utiliser `test@example.com` / `admin`

## Production

**Backend** :
- Changer `JWT_SECRET` en production
- Configurer CORS avec origins spécifiques
- Utiliser HTTPS
- Configurer reverse proxy (nginx)

**Flutter** :
- Build avec `--release`
- Passer l'URL prod via `--dart-define`
- Utiliser HTTPS

## Documentation

- Backend : [backend/README.md](backend/README.md)
- Flutter : [app/README.md](app/README.md)
- FastAPI Docs : http://localhost:8000/docs

## Support

Questions ou problèmes ? Consultez les README détaillés dans chaque dossier.
