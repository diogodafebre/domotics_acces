#!/usr/bin/env python3
"""
Script de vérification de la configuration backend.
Lance ce script pour vérifier que tout est bien configuré.
"""

import sys
import os

def check_env_file():
    """Vérifie que le fichier .env existe."""
    if not os.path.exists('.env'):
        print("❌ Fichier .env non trouvé")
        print("   → Exécuter: cp .env.example .env")
        return False
    print("✅ Fichier .env trouvé")
    return True

def check_dependencies():
    """Vérifie que les dépendances Python sont installées."""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import jose
        import passlib
        import pydantic
        print("✅ Dépendances Python installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendances manquantes: {e}")
        print("   → Exécuter: pip install -r requirements.txt")
        return False

def check_database_connection():
    """Vérifie la connexion à la base de données."""
    try:
        from dotenv import load_dotenv
        load_dotenv()

        from sqlalchemy import create_engine
        from app.core.config import settings

        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1"))
            result.fetchone()
        print("✅ Connexion MySQL réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion MySQL: {e}")
        print("   → Vérifier les paramètres DB dans .env")
        print("   → Vérifier que MySQL est lancé")
        return False

def check_tables():
    """Vérifie que les tables existent."""
    try:
        from dotenv import load_dotenv
        load_dotenv()

        from sqlalchemy import create_engine, inspect
        from app.core.config import settings

        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        required_tables = ['users', 'acces_app', 'abonnement']
        missing = [t for t in required_tables if t not in tables]

        if missing:
            print(f"❌ Tables manquantes: {', '.join(missing)}")
            print("   → Créer les tables dans MySQL")
            return False

        print("✅ Toutes les tables existent (users, acces_app, abonnement)")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des tables: {e}")
        return False

def check_test_user():
    """Vérifie que l'utilisateur de test existe."""
    try:
        from dotenv import load_dotenv
        load_dotenv()

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.core.config import settings
        from app.db.models import AccesApp, User

        engine = create_engine(settings.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        acces = session.query(AccesApp).filter_by(email='test@example.com').first()
        user = session.query(User).filter_by(email='test@example.com').first()

        session.close()

        if not acces or not user:
            print("❌ Utilisateur de test non trouvé")
            print("   → Exécuter: mysql -u root -p move_acces < seed.sql")
            return False

        print("✅ Utilisateur de test existe (test@example.com)")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de l'utilisateur: {e}")
        return False

def generate_test_hash():
    """Génère un hash bcrypt pour 'admin'."""
    try:
        from passlib.hash import bcrypt
        hash_value = bcrypt.hash("admin")
        print(f"\n📝 Hash bcrypt pour 'admin':")
        print(f"   {hash_value}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la génération du hash: {e}")
        return False

def main():
    print("🔍 Vérification de la configuration Backend\n")
    print("=" * 50)

    checks = [
        ("Fichier .env", check_env_file),
        ("Dépendances Python", check_dependencies),
        ("Connexion MySQL", check_database_connection),
        ("Tables MySQL", check_tables),
        ("Utilisateur de test", check_test_user),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur inattendue lors de '{name}': {e}")
            results.append(False)
        print()

    print("=" * 50)

    if all(results):
        print("✅ Tout est prêt ! Vous pouvez lancer le serveur:")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n📚 Documentation API: http://localhost:8000/docs")
        generate_test_hash()
        return 0
    else:
        print("❌ Des problèmes ont été détectés. Corrigez-les avant de lancer le serveur.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
