from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """
    Defines the 'users' table in MySQL.
    Stores account credentials and links to user-specific expenses.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Relationship: Deleting a user will automatically delete all their expenses (cascade)
    expenses = relationship("Expense", back_populates="owner", cascade="all, delete-orphan")


class Expense(Base):
    """
    Defines the 'expenses' table in MySQL.
    Stores individual transaction details linked to a specific user.
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)

    # Relationship: Links back to the User model object
    owner = relationship("User", back_populates="expenses")