"""Models for Users API."""

from typing import Self

from pydantic import BaseModel, EmailStr, RootModel, model_validator

from server.model_utils import EmptyPatchError, ObjectIdStr, SelfIdStr


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

    @model_validator(mode="after")
    def _is_non_empty(self) -> Self:
        if self.name is None and self.email is None:
            raise EmptyPatchError

        return self


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
