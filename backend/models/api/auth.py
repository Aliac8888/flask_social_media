from pydantic import BaseModel, EmailStr, RootModel

from models.api.user import User
from models.mongo import ObjectIdStr


class AuthnRequest(BaseModel):
    email: EmailStr
    password: str


class AuthnResponse(BaseModel):
    user: User
    jwt: str


class AuthnExpired(BaseModel):
    type: str = "AuthnExpired"
    message: str = "JWT authentication token is expired"
    details: str


class AuthnInvalid(BaseModel):
    type: str = "AuthnInvalid"
    message: str = "JWT authentication token is invalid"
    details: str


class AuthnMissing(BaseModel):
    type: str = "AuthnMissing"
    message: str = "JWT authentication token is missing"
    details: str


class AuthnIdentity(BaseModel):
    user_id: ObjectIdStr
    admin: bool


UserPassword = RootModel[str]

AuthnFailed = RootModel[AuthnExpired | AuthnInvalid | AuthnMissing]


class AuthzFailed(BaseModel):
    type: str = "AuthzFailed"
    message: str = "User cannot access this resource"
