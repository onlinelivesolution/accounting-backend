from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    try:
        print("VERIFY INPUT:", repr(plain_password))
        print("VERIFY HASH:", repr(hashed_password))

        result = pwd_context.verify(plain_password.strip(), hashed_password.strip())

        print("VERIFY RESULT:", result)

        return result

    except Exception as e:
        print("VERIFY ERROR:", str(e))
        return False
