from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials # type: ignore
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token")
        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide access token")

        return token_data # type: ignore

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None
        
    