# Domotics Access - Application Mobile Flutter

Application mobile Android/iOS avec authentification JWT pour accéder au backend Domotics.

## Technologies

- **Flutter 3.0+** - Framework multi-plateforme
- **Dio** - Client HTTP avec intercepteurs
- **Provider** - Gestion d'état
- **flutter_secure_storage** - Stockage sécurisé des tokens JWT
- **Material 3** - Design moderne

## Structure

```
app/
├── lib/
│   ├── main.dart                  # Point d'entrée de l'app
│   ├── models/
│   │   └── user.dart              # Modèle User
│   ├── pages/
│   │   ├── login_page.dart        # Page de connexion
│   │   └── dashboard_page.dart    # Dashboard après connexion
│   ├── services/
│   │   └── api_client.dart        # Client API avec JWT et refresh
│   └── state/
│       └── auth_state.dart        # Gestion d'état authentification
├── pubspec.yaml
└── README.md
```

## Fonctionnalités

### 1. Authentification
- Login avec email/password
- Validation des champs (email, password non vide)
- Stockage sécurisé des tokens JWT (access + refresh)
- Gestion automatique du refresh token
- Logout avec suppression des tokens

### 2. Dashboard
- Affichage des informations utilisateur (GET /auth/me)
- Pull-to-refresh pour mettre à jour les données
- Déconnexion avec confirmation

### 3. Gestion des erreurs
- Messages d'erreur clairs (Snackbar)
- Gestion des erreurs 401 (refresh automatique)
- Redirection vers login si refresh échoue

## Installation

### Prérequis

- Flutter SDK 3.0+
- Backend FastAPI lancé et accessible

### 1. Installer les dépendances

```bash
flutter pub get
```

### 2. Configuration de l'API

L'URL de l'API backend doit être passée via `--dart-define` au moment du lancement.

Par défaut : `http://localhost:8000`

### 3. Lancer l'application

#### En local (iOS Simulator / Android Emulator)

```bash
# Avec backend local
flutter run --dart-define=API_BASE_URL=http://localhost:8000

# Avec backend sur réseau local (remplacer <ip> par l'IP de votre machine)
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000
```

#### Sur device physique Android

**IMPORTANT** : Remplacer `localhost` par l'adresse IP de votre machine sur le réseau local.

```bash
# Trouver l'IP de votre machine
# macOS/Linux: ifconfig | grep inet
# Windows: ipconfig

# Lancer avec l'IP
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000
```

#### Sur device physique iOS

Pour iOS, utiliser l'IP de votre machine (pas `localhost`).

```bash
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000
```

## Flux d'authentification

1. **Lancement de l'app**
   - Vérification de la présence de tokens stockés
   - Si présents : appel GET /auth/me pour valider
   - Si valide : affichage Dashboard
   - Sinon : affichage Login

2. **Login**
   - Saisie email + password
   - POST /auth/login
   - Succès : stockage tokens + navigation Dashboard
   - Échec : affichage erreur

3. **Navigation protégée**
   - Toutes les requêtes incluent `Authorization: Bearer <access>`
   - Si 401 : tentative refresh automatique
   - Si refresh OK : retry de la requête
   - Si refresh KO : logout + retour Login

4. **Refresh automatique**
   - Intercepteur Dio détecte les 401
   - POST /auth/refresh avec refresh token
   - Mise à jour du access token en storage
   - Retry de la requête originale

5. **Logout**
   - Suppression des tokens du secure storage
   - Retour automatique à Login

## Compte de test

Les identifiants de test sont affichés sur la page de login :

- **Email** : `test@example.com`
- **Mot de passe** : `admin`

## Build de production

### Android APK

```bash
flutter build apk --release --dart-define=API_BASE_URL=https://votre-api.com
```

### Android App Bundle (Google Play)

```bash
flutter build appbundle --release --dart-define=API_BASE_URL=https://votre-api.com
```

### iOS

```bash
flutter build ios --release --dart-define=API_BASE_URL=https://votre-api.com
```

## Dépendances principales

```yaml
dependencies:
  dio: ^5.4.0                        # Client HTTP
  flutter_secure_storage: ^9.0.0    # Stockage sécurisé
  provider: ^6.1.1                   # State management
```

## Sécurité

- Tokens stockés dans **flutter_secure_storage** (Keychain iOS / Keystore Android)
- Aucun stockage en clair des mots de passe
- Refresh automatique pour limiter l'exposition du access token
- HTTPS recommandé en production

## Troubleshooting

### Erreur "Connection refused" sur Android

Si vous obtenez une erreur de connexion sur Android :

1. Vérifiez que le backend est accessible depuis votre réseau
2. Utilisez l'IP de votre machine (pas `localhost` ni `127.0.0.1`)
3. Pour l'émulateur Android : utilisez `10.0.2.2` au lieu de `localhost`

```bash
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

### Erreur "Invalid credentials"

1. Vérifiez que le backend est lancé
2. Vérifiez que les données de seed.sql ont été importées
3. Utilisez les bons identifiants : `test@example.com` / `admin`

### Tokens expirés

Les tokens sont automatiquement rafraîchis. Si vous obtenez une erreur :

1. Déconnectez-vous
2. Reconnectez-vous
3. Vérifiez que le refresh token n'est pas expiré (15 jours)

## Support

Documentation Flutter : https://flutter.dev/docs
Documentation Dio : https://pub.dev/packages/dio
