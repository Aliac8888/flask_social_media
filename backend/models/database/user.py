from pydantic import BaseModel, EmailStr, RootModel

from models.database.mongo import ObjectIdRaw, SelfIdRaw


class DbUser(BaseModel):
    _id: SelfIdRaw
    name: str
    email: EmailStr
    credential: bytes
    followings: list[ObjectIdRaw]


class DbUserNotFoundError(Exception):
    pass


class DbUserExistsError(Exception):
    pass


DbUserList = RootModel[list[DbUser]]
