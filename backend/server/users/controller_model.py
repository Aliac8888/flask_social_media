from pydantic import BaseModel, EmailStr, RootModel

from server.model_utils import ObjectIdRaw, SelfIdRaw


class DbUser(BaseModel):
    id: SelfIdRaw
    name: str
    email: EmailStr
    credential: bytes
    followings: list[ObjectIdRaw]


class DbUserNotFoundError(Exception):
    pass


class DbUserExistsError(Exception):
    pass


DbUserList = RootModel[list[DbUser]]
