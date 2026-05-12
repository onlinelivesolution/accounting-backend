# common/utils/jwt_handler.py

from jose import jwt
from datetime import datetime, timedelta

# 🔐 SECRET KEY
SECRET_KEY = "my_super_secret_erp_key_2026"

# 🔐 ALGORITHM
ALGORITHM = "HS256"

# 🔐 TOKEN EXPIRE
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
