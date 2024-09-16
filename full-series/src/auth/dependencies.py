from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import Any, List
from .models import User

user_service = UserService()
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials # type: ignore
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token")
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"errror":"Invalid or expired token",                        "result": "Please get new token"})
        self.verify_token_data(token_data)
        return token_data # type: ignore
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this error in child classes")

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None
        
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide access token")
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide refresh token")
        
async def get_current_user(token_details: dict=Depends(AccessTokenBearer()), session: AsyncSession= Depends(get_session)):
    user_email = token_details['user']['email']
    return await user_service.get_user_by_email(user_email, session)


class RoleChecker:
    def __init__(self, allowed_roles:List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this action")
    