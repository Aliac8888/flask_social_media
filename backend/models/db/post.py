from datetime import datetime

from pydantic import BaseModel, RootModel

from models.db.mongo import SelfIdRaw
from models.db.user import DbUser


class DbPost(BaseModel):
    _id: SelfIdRaw
    content: str
    creation_time: datetime
    modification_time: datetime
    author: DbUser


class DbPostNotFoundError(Exception):
    pass


DbPostList = RootModel[list[DbPost]]
