from datetime import datetime

from pydantic import BaseModel, RootModel

from models.db.user import DbUser
from models.mongo import SelfIdRaw


class DbPost(BaseModel):
    id: SelfIdRaw
    content: str
    creation_time: datetime
    modification_time: datetime
    author: DbUser


class DbPostNotFoundError(Exception):
    pass


DbPostList = RootModel[list[DbPost]]
