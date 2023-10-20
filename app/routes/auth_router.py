from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from fastapi import APIRouter


from app.service.auth_service import AuthService

authService = AuthService()
class Credential(BaseModel):
   username: str
   password: str
   class Config:
        schema_extra = {
            "username": {
                "username",
            },
            "password": {
                "password",
            },

        }

router = APIRouter()


@router.post("/token", name='Login' , response_class=PlainTextResponse)
async def login( credential : Credential):
        """
        Login:
        - **username**: the user's username (required)
        - **password**: the user's password (required)
        """
        u= authService.authenticate_cognito_user(str(credential.username),str(credential.password))
        return u


