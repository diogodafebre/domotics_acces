"""SQLAlchemy models mapping existing MySQL tables."""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class AccesApp(Base):
    """Table storing app access credentials with bcrypt hashed passwords."""
    __tablename__ = "acces_app"

    email = Column(String(254), primary_key=True, index=True)
    password_hash = Column(String(255), nullable=False)


class User(Base):
    """User profile information."""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=True)
    prenom = Column(String(100), nullable=True)
    date_naissance = Column(Date, nullable=True)
    rue = Column(String(200), nullable=True)
    npa = Column(String(10), nullable=True)
    localite = Column(String(100), nullable=True)
    tel = Column(String(20), nullable=True)
    email = Column(String(254), nullable=True, unique=True, index=True)

    # Relationship to abonnement
    abonnements = relationship("Abonnement", back_populates="user")


class Abonnement(Base):
    """Subscription information."""
    __tablename__ = "abonnement"

    abo_id = Column(Integer, primary_key=True, autoincrement=True)
    abo_id_actual = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    abo_state = Column(String(50), nullable=True)
    abo_name = Column(String(100), nullable=True)
    abo_date_start = Column(Date, nullable=True)
    abo_date_creation = Column(DateTime, nullable=True)
    abo_date_stop = Column(Date, nullable=True)
    abo_duration = Column(Integer, nullable=True)
    abo_renew = Column(Boolean, nullable=True)
    abo_price = Column(Numeric(10, 2), nullable=True)
    abo_discount = Column(Numeric(10, 2), nullable=True)
    abo_slices = Column(Integer, nullable=True)
    abo_price_finances = Column(Numeric(10, 2), nullable=True)

    # Relationship to user
    user = relationship("User", back_populates="abonnements")
