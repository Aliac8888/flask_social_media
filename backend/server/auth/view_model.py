"""Models of Authentication/Authorization API."""

from pydantic import BaseModel, EmailStr, RootModel

from server.model_utils import ObjectIdStr
from server.users.view_model import User


class AuthnRequest(BaseModel):
    """Authentication (login) request."""

    email: EmailStr
    password: str


class AuthnResponse(BaseModel):
    """Authentication response."""

    user: User
    jwt: str


class AuthnExpired(BaseModel):
    """Authentication token is expired."""

    type: str = "AuthnExpired"
    message: str = "JWT authentication token is expired"
    details: str


class AuthnInvalid(BaseModel):
    """Authentication token is invalid."""

    type: str = "AuthnInvalid"
    message: str = "JWT authentication token is invalid"
    details: str


class AuthnMissing(BaseModel):
    """Authentication token is missing."""

    type: str = "AuthnMissing"
    message: str = "JWT authentication token is missing"
    details: str


class AuthnIdentity(BaseModel):
    """Authentication Identity."""

    user_id: ObjectIdStr
    admin: bool


UserPassword = RootModel[str]
"""Password of a user."""

AuthnFailed = RootModel[AuthnExpired | AuthnInvalid | AuthnMissing]
"""Authentication failed."""


class AuthzFailed(BaseModel):
    """Authorization failed."""

    type: str = "AuthzFailed"
    message: str = "User cannot access this resource"
