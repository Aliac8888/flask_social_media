from pydantic import BaseModel

from models.api.mongo import ObjectIdStr, SelfIdStr
from models.api.temporal import Instant
from models.api.user import User


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
    message: str = "Post not found"


class PostsList(BaseModel):
    posts: list[Post]
