from datetime import datetime

from pydantic import BaseModel, RootModel

from models.database.mongo import SelfIdRaw
from models.database.user import DbUser


class DbPost(BaseModel):
    _id: SelfIdRaw
    content: str
    creation_time: datetime
    modification_time: datetime
    author: DbUser


class DbPostNotFoundError(Exception):
    pass


DbPostList = RootModel[list[DbPost]]
