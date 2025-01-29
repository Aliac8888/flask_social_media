from typing import Self

from pydantic import BaseModel, EmailStr, RootModel, model_validator

from server.model_utils import EmptyPatchError, ObjectIdStr, SelfIdStr


class User(BaseModel):
    id: SelfIdStr
    name: str
    email: EmailStr


class UserInit(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

    @model_validator(mode="after")
    def is_non_empty(self) -> Self:
        if self.name is None and self.email is None:
            raise EmptyPatchError

        return self


class UserId(BaseModel):
    user_id: ObjectIdStr


class UserNotFound(BaseModel):
    type: str = "UserNotFound"
    message: str = "User not found"


class UserExists(BaseModel):
    type: str = "UserExists"
    message: str = "User already exists"


UsersList = RootModel[list[User]]
