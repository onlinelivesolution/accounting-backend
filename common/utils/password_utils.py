# common/utils/password_utils.py
from passlib.context import CryptContext

# ✅ Argon2 officially supported scheme name is "argon2"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate an Argon2 hash from the provided plain text password."""
    return pwd_context.hash(password)
