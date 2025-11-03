"""Seed database with test data."""
import asyncio
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal
from app.models.abonnement import Abonnement
from app.models.acces_app import AccesApp
from app.models.user import User
from app.security.passwords import hash_password


async def seed_database():
    """Seed database with initial test data."""
    async with AsyncSessionLocal() as session:
        print("🌱 Seeding database...")

        # Check if user already exists
        from sqlalchemy import select

        result = await session.execute(select(User).where(User.email == "diogofebre@gmail.com"))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("✓ Test user already exists, skipping seed")
            return

        # Create test user
        user = User(
            nom="Febre",
            prenom="Diogo",
            date_naissance=date(2003, 12, 1),
            rue="Rue de la Paalud 27",
            npa="1955",
            localite="Chamoson",
            tel="0767039712",
            email="diogofebre@gmail.com",
        )
        session.add(user)
        await session.flush()

        # Create access credentials (password: TestPassword123!)
        acces = AccesApp(
            email="diogofebre@gmail.com",
            password_hash=hash_password("TestPassword123!"),
        )
        session.add(acces)

        # Create active subscription
        today = date.today()
        subscription = Abonnement(
            user_id=user.user_id,
            abo_state="active",
            abo_name="Mensuel Basic",
            abo_date_start=today,
            abo_date_stop=today + timedelta(days=30),
            abo_duration=30,
            abo_price=49.90,
            abo_discount=0.00,
            abo_renew=1,
        )
        session.add(subscription)

        await session.commit()

        print("✓ Seeded test user:")
        print(f"  Email: diogofebre@gmail.com")
        print(f"  Password: TestPassword123!")
        print(f"  User ID: {user.user_id}")
        print(f"  Subscription: {subscription.abo_name} ({subscription.abo_state})")
        print("🌱 Database seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
