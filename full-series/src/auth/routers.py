from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer
from datetime import datetime

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 7

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session) # type: ignore
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return await user_service.create_user(user_data, session)# type: ignore


@auth_router.post("/login", response_model=UserModel)
async def login(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session) # type: ignore
    if user is not None:
        if passsword_valid := verify_password(password, user.password_hash):
            access_token = create_access_token(user_data={
                'email': user.email,
                'user_uid': str(user.uid)
            }, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)) # type: ignore
            refresh_token=create_access_token(user_data={
                'email': user.email,
                'user_uid': str(user.uid)
            }, refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)) # type: ignore

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password")

@auth_router.post("/refresh-token", response_model=UserModel)
async def get_new_acces_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        ) # type: ignore
        return JSONResponse(content={"access_token": new_access_token})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
