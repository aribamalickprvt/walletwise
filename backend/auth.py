from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import hashlib
import secrets

SECRET_KEY = "SUPER_SECRET_RANDOM_STRING_FOR_INTERNSHIP_PROJECT"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    """Converts a plain text password into a secure hash using built-in hashlib."""
    # Using SHA-256 with a simple text hash for development stability
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a plain text password with a stored hash."""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    """Generates a secure JWT token for session persistence."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt