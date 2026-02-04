# common/utils/security.py
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from typing import Tuple

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # add argon2 first (primary)
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> Tuple[bool, bool]:
    """
    Verify password and return (is_valid, needs_rehash)
    - If hash is old/plaintext, verify and flag to upgrade.
    """
    if not hashed_password:
        return False, False

    try:
        # Verify with Argon2 (normal)
        is_valid = pwd_context.verify(plain_password, hashed_password)
        # Check if rehashing is recommended (e.g. config changed)
        needs_rehash = pwd_context.needs_update(hashed_password)
        return is_valid, needs_rehash

    except UnknownHashError:
        # Old plaintext or unrecognized format
        if plain_password == hashed_password:
            # valid, but must rehash
            return True, True
        return False, False

    except Exception:
        return False, False
