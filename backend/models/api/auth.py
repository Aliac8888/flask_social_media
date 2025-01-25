from pydantic import BaseModel, EmailStr

from models.api.mongo import ObjectIdStr
from models.api.user import User


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
