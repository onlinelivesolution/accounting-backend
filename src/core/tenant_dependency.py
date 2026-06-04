from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from common.utils.jwt_handler import decode_access_token

from src.core.tenant_database import get_tenant_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_tenant_db(token: str = Depends(oauth2_scheme)):

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(status_code=401, detail="Invalid Token")

    database_name = payload.get("tenant")

    if not database_name:

        raise HTTPException(status_code=401, detail="Tenant Missing")

    db = get_tenant_session(database_name)

    try:

        yield db

    finally:

        await db.close()
