"""Models for Users API."""

from pydantic import BaseModel, EmailStr, RootModel

from server.model_utils import ObjectIdStr, SelfIdStr


class User(BaseModel):
    """Signed-up user."""

    id: SelfIdStr
    name: str
    email: EmailStr


class UserInit(BaseModel):
    """User to be signed up."""

    name: str
    email: EmailStr
    password: str


class UserPatch(BaseModel):
    """User modifications."""

    name: str | None = None
    email: EmailStr | None = None


class UserId(BaseModel):
    """Id of a User."""

    user_id: ObjectIdStr


class UserNotFound(BaseModel):
    """Request referred to a user which did not exist."""

    type: str = "UserNotFound"
    message: str = "User not found"


class UserExists(BaseModel):
    """Request tries to define a user which already exists."""

    type: str = "UserExists"
    message: str = "User already exists"


UsersList = RootModel[list[User]]
"""List of users."""
