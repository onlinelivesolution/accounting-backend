from datetime import timedelta
from fastapi import HTTPException, status
from src.schemas.loginschema import LoginRequest, LoginResponse, UserInfoSchema
from src.repositories.interfaces.ilogin_repository import ILoginRepository
from src.services.interfaces.ilogin_service import ILoginService
from common.utils.jwt_handler import create_access_token


ACCESS_TOKEN_EXPIRE_HOURS = 12


class LoginService(ILoginService):
    def __init__(self, repository: ILoginRepository):
        self.repository = repository

    async def login(self, request: LoginRequest) -> LoginResponse:
        # ✅ Step 1: Authenticate user
        user = await self.repository.authenticate_user(request.userName, request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        # ✅ Step 2: Fetch role permissions
        permissions = await self.repository.get_user_permissions(user.roleID)

        # ✅ Step 3: Generate JWT
        token = create_access_token(
            data={"sub": user.userName},
            expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        )

        # ✅ Step 4: Convert SQLAlchemy model to Pydantic schema using from_attributes
        user_data = UserInfoSchema.model_validate(user)

        # ✅ Step 5: Return complete login response
        return LoginResponse(
            token=token,
            user=user_data,
            permissions=permissions
        )
