from passlib.context import CryptContext
from passlib.hash import argon2

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    try:
        plain_password = plain_password.strip()
        hashed_password = hashed_password.strip()

        print("VERIFY INPUT:", repr(plain_password))
        print("VERIFY HASH:", repr(hashed_password))

        result = argon2.verify(plain_password, hashed_password)

        print("VERIFY RESULT:", result)

        return result

    except Exception as e:
        print("VERIFY ERROR:", str(e))
        return False


def hash_password(password: str):
    return argon2.hash(password)
