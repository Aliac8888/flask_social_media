from datetime import datetime

from pydantic import BaseModel, RootModel

from models.mongo import ObjectIdRaw, SelfIdRaw


class DbComment(BaseModel):
    id: SelfIdRaw
    content: str
    author: ObjectIdRaw
    post: ObjectIdRaw
    creation_time: datetime
    modification_time: datetime


class DbCommentNotFoundError(Exception):
    pass


DbCommentList = RootModel[list[DbComment]]
