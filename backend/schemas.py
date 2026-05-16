from pydantic import BaseModel, Field
from datetime import date

# ==========================================
# USER SCHEMAS
# ==========================================

class UserCreate(BaseModel):
    """Validates incoming payload when a user registers."""
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
class Token(BaseModel):
    """Structure of the response when a user successfully logs in."""
    access_token: str
    token_type: str
class TokenData(BaseModel):
    """Internal helper schema to check the validated user inside a token."""
    username: str | None = None


# ==========================================
# EXPENSE SCHEMAS
# ==========================================

class ExpenseBase(BaseModel):
    """Shared fields for creating or reading expenses."""
    amount: float = Field(..., gt=0, description="The expense amount must be greater than 0")
    category: str = Field(..., min_length=1, max_length=50)
    date: date
    description: str | None = Field(None, max_length=255)

class ExpenseCreate(ExpenseBase):
    """Validates data coming from the frontend form when adding an expense."""
    pass  # It inherits everything from ExpenseBase directly

class ExpenseResponse(ExpenseBase):
    """Formats the data sent back to the frontend (includes DB fields)."""
    id: int
    user_id: int

    class Config:
        # Crucial for SQLAlchemy compatibility: allows Pydantic to read ORM objects
        from_attributes = True