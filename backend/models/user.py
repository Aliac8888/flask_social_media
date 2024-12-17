from pydantic import BaseModel, EmailStr, model_validator
from models.mongo import ObjectIdStr


class User(BaseModel):
    name: str
    email: EmailStr


class UserInit(BaseModel):
    name: str
    email: EmailStr


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

    @model_validator(mode="after")
    def is_non_empty(self):
        if self.name is None and self.email is None:
            raise ValueError("patch is empty")

        return self


class UserId(BaseModel):
    user_id: ObjectIdStr


class UserWithId(User):
    id: ObjectIdStr


class UserWithFriends(UserWithId):
    friends: list[UserWithId]


class UserNotFound(BaseModel):
    message: str = "User not found"


class UserExists(BaseModel):
    message: str = "User already exists"


class UsersList(BaseModel):
    users: list[UserWithId]
