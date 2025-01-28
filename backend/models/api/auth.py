from pydantic import BaseModel, EmailStr

from models.api.user import User
from models.mongo import ObjectIdStr


class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user: User
    jwt: str


class AuthFailed(BaseModel):
    type: str = "AuthFailed"
    message: str = "Authentication failed"


class JwtIdentity(BaseModel):
    user_id: ObjectIdStr
    admin: bool


class UserPasswordPatch(BaseModel):
    password: str
