from pydantic import BaseModel, RootModel

from models.api.temporal import Instant
from models.api.user import User
from models.mongo import ObjectIdStr, SelfIdStr


class Post(BaseModel):
    id: SelfIdStr
    content: str
    creation_time: Instant
    modification_time: Instant
    author: User


class PostInit(BaseModel):
    content: str
    author: ObjectIdStr


class PostPatch(BaseModel):
    content: str


class PostQuery(BaseModel):
    author_id: ObjectIdStr | None = None


class PostId(BaseModel):
    post_id: ObjectIdStr


class PostNotFound(BaseModel):
    type: str = "PostNotFound"
    message: str = "Post not found"


PostsList = RootModel[list[Post]]
