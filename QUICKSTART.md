# 🚀 Quickstart - Test en < 15 min

Guide rapide pour tester la V1 complète (Backend + Flutter).

## Prérequis

- Python 3.11+ installé
- Flutter SDK installé
- MySQL avec la base `move_acces` existante
- Les 3 tables créées : `users`, `acces_app`, `abonnement`

## Étape 1 : Backend (5 min)

```bash
cd backend

# 1. Copier la config
cp .env.example .env

# 2. Éditer .env avec vos paramètres MySQL
# DB_HOST=127.0.0.1
# DB_USER=root
# DB_PASS=votre_mot_de_passe
# DB_NAME=move_acces
# JWT_SECRET=changez_moi

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Importer les données de test
mysql -u root -p move_acces < seed.sql
# Cela crée un utilisateur : test@example.com / admin

# 5. Lancer le serveur
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **Vérification** : Ouvrir http://localhost:8000/docs → Vous devez voir la documentation Swagger

## Étape 2 : Tester l'API (2 min)

Dans un nouveau terminal ou via http://localhost:8000/docs :

```bash
# Test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"admin"}'

# Doit retourner :
# {"access":"eyJ...","refresh":"eyJ...","user":{...}}

# Copier le access token et tester /me
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <COLLER_LE_TOKEN_ICI>"

# Doit retourner :
# {"id":1,"email":"test@example.com","prenom":"Alice","nom":"Dupont"}
```

## Étape 3 : Flutter App (5 min)

**Terminal 1** : Backend doit tourner sur port 8000

**Terminal 2** : Lancer l'app Flutter

```bash
cd app

# 1. Installer les dépendances
flutter pub get

# 2. Lancer l'app
# Sur émulateur iOS/Android :
flutter run --dart-define=API_BASE_URL=http://localhost:8000

# Sur device physique Android :
# Trouver votre IP locale (ex: 192.168.1.100)
# macOS/Linux: ifconfig | grep "inet " | grep -v 127.0.0.1
# Windows: ipconfig
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000

# Sur émulateur Android seulement :
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

## Étape 4 : Tester le flux complet (3 min)

1. **Login**
   - Saisir : `test@example.com`
   - Mot de passe : `admin`
   - Cliquer "Se connecter"
   - ✅ Doit naviguer vers Dashboard

2. **Dashboard**
   - ✅ Affiche "Bienvenue, Alice Dupont"
   - ✅ Affiche l'email et l'ID
   - Tirer vers le bas pour refresh → ✅ Recharge les données

3. **Logout**
   - Cliquer sur le bouton "Se déconnecter"
   - Confirmer
   - ✅ Retour à la page Login

4. **Test erreur**
   - Saisir un mauvais mot de passe
   - ✅ Message d'erreur en rouge : "Identifiants invalides"

## Vérifications des critères d'acceptation

- ✅ Backend démarre sans erreur
- ✅ POST /auth/login retourne tokens + user info
- ✅ GET /auth/me refuse sans Bearer (401)
- ✅ GET /auth/me fonctionne avec Bearer valide
- ✅ Flutter stocke les tokens (vérifiable en tuant l'app et redémarrant → reste connecté)
- ✅ Refresh automatique (vérifiable en attendant 15 min ou en invalidant le token)
- ✅ UX propre avec loading et gestion d'erreurs

## Troubleshooting rapide

### Backend : Erreur MySQL
```bash
# Vérifier que MySQL tourne
mysql -u root -p -e "SHOW DATABASES;"

# Vérifier que la base existe
mysql -u root -p -e "USE move_acces; SHOW TABLES;"
```

### Flutter : Connection refused
```bash
# Sur device physique, utiliser l'IP réseau (pas localhost)
ifconfig | grep "inet "  # Trouver votre IP (ex: 192.168.1.100)

# Relancer avec la bonne IP
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000
```

### "Invalid credentials"
```bash
# Réimporter les données de test
cd backend
mysql -u root -p move_acces < seed.sql
```

## Générer un nouveau mot de passe bcrypt

```python
python3 -c "from passlib.hash import bcrypt; print(bcrypt.hash('nouveau_mdp'))"
```

Puis l'insérer dans MySQL :

```sql
INSERT INTO acces_app (email, password_hash)
VALUES ('nouvel@email.com', '$2b$12$...');

INSERT INTO users (email, nom, prenom)
VALUES ('nouvel@email.com', 'Nom', 'Prenom');
```

## Notes importantes

- **Access token** : expire après 15 minutes (refresh automatique)
- **Refresh token** : expire après 15 jours
- **Tokens stockés** : flutter_secure_storage (Keychain iOS / Keystore Android)
- **CORS** : activé en mode `*` pour le dev (à restreindre en prod)

## Prochaines étapes

Une fois la V1 validée :
- Ajouter d'autres endpoints (profil complet, abonnements, etc.)
- Implémenter la gestion des abonnements
- Ajouter des tests unitaires
- Configurer CI/CD
- Déployer en production

---

**Temps total estimé** : 10-15 minutes
**Questions** : Consulter les README détaillés dans `backend/` et `app/`
