"""SQLAlchemy models mapping existing MySQL tables."""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, Boolean, BigInteger
from sqlalchemy.orm import relationship

from app.db.session import Base


class AccesApp(Base):
    """Table storing app access credentials with bcrypt hashed passwords."""
    __tablename__ = "acces_app"

    user_email = Column(String(191), primary_key=True, index=True)
    acces_password = Column(String(255), nullable=False)


class User(Base):
    """User profile information."""
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_nom = Column(String(100), nullable=False)
    user_prenom = Column(String(100), nullable=False)
    user_date_naissance = Column(Date, nullable=False)
    user_rue = Column(String(150), nullable=True)
    user_npa = Column(String(4), nullable=True)
    user_localite = Column(String(100), nullable=True)
    user_telephone = Column(String(20), nullable=True)
    user_mobile = Column(String(20), nullable=True)
    user_email = Column(String(191), nullable=False, unique=True, index=True)

    # Relationship to abonnement
    abonnements = relationship("Abonnement", back_populates="user")


class Abonnement(Base):
    """Subscription information."""
    __tablename__ = "abonnement"

    abo_id = Column(Integer, primary_key=True, autoincrement=True)
    abo_id_actual = Column(Integer, nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=True)
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
