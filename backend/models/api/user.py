from typing import Self

from pydantic import BaseModel, EmailStr, RootModel, model_validator

from models.api.error import EmptyPatchError
from models.api.mongo import ObjectIdStr, SelfIdStr


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
    password: str | None = None

    @model_validator(mode="after")
    def is_non_empty(self) -> Self:
        if self.name is None and self.email is None and self.password is None:
            raise EmptyPatchError

        return self


class UsersQuery(BaseModel):
    following_id: ObjectIdStr | None = None


class UserId(BaseModel):
    user_id: ObjectIdStr


class Following(BaseModel):
    follower_id: ObjectIdStr
    following_id: ObjectIdStr


class UserNotFound(BaseModel):
    type: str = "UserNotFound"
    message: str = "User not found"


class UserExists(BaseModel):
    type: str = "UserExists"
    message: str = "User already exists"


UsersList = RootModel[list[User]]
