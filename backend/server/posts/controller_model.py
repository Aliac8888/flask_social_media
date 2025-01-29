from datetime import datetime

from pydantic import BaseModel, RootModel

from server.model_utils import SelfIdRaw
from server.users.controller_model import DbUser


class DbPost(BaseModel):
    id: SelfIdRaw
    content: str
    creation_time: datetime
    modification_time: datetime
    author: DbUser


class DbPostNotFoundError(Exception):
    pass


DbPostList = RootModel[list[DbPost]]
