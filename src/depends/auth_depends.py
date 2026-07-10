# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from jose import jwt, JWTError

# SECRET_KEY = "YOUR_SECRET_KEY"
# ALGORITHM = "HS256"

# security = HTTPBearer()


# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ):

#     token = credentials.credentials

#     try:

#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         return payload

#     except JWTError:

#         raise HTTPException(status_code=401, detail="Invalid token")


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from common.utils.jwt_handler import decode_access_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    print("JWT PAYLOAD:", payload)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
