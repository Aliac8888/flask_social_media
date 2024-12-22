from pydantic import BaseModel
from models.mongo import ObjectIdStr, SelfIdStr
from models.datetime import DateTime


class Post(BaseModel):
    id: SelfIdStr
    content: str
    creation_time: DateTime
    modification_time: DateTime
    author: ObjectIdStr


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
