"""Controller Models for Users."""

from pydantic import BaseModel, EmailStr, RootModel

from server.model_utils import ObjectIdRaw, SelfIdRaw


class DbUser(BaseModel):
    """User database schema."""

    id: SelfIdRaw
    name: str
    email: EmailStr
    credential: bytes
    followings: list[ObjectIdRaw]


class DbUserNotFoundError(Exception):
    """User was not found in the database."""


class DbUserExistsError(Exception):
    """User was already in the database."""


DbUserList = RootModel[list[DbUser]]
"""List of database users."""
