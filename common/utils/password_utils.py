from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt", "argon2"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    try:
        plain_password = plain_password.strip()
        hashed_password = hashed_password.strip()

        result = pwd_context.verify(plain_password, hashed_password)

        print("VERIFY RESULT:", result)
        print("TYPE:", type(result))

        return result

    except Exception as e:
        print("VERIFY ERROR:", str(e))
        return False
