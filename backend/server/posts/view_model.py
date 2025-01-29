from pydantic import BaseModel, RootModel

from server.model_utils import Instant, ObjectIdStr, SelfIdStr
from server.users.view_model import User


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
