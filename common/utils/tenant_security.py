import bcrypt
from typing import Tuple

# =====================================
# HASH PASSWORD
# =====================================


def hash_password(password: str) -> str:

    if not isinstance(password, str):
        raise ValueError(f"Password must be string, got {type(password)}")

    password = password.strip()

    if not password:
        raise ValueError("Password cannot be empty")

    # bcrypt limit safety
    password = password[:72]

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed.decode("utf-8")


# =====================================
# VERIFY PASSWORD
# =====================================


def verify_password(plain_password: str, hashed_password: str) -> Tuple[bool, bool]:

    try:

        if not plain_password or not hashed_password:
            return False, False

        plain_password = str(plain_password).strip()

        # bcrypt safe limit
        plain_password = plain_password[:72]

        is_valid = bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

        # no rehash logic for now
        needs_rehash = False

        return is_valid, needs_rehash

    except Exception as e:

        print("VERIFY ERROR:", str(e))

        return False, False
