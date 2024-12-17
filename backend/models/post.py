from typing import Annotated
from pydantic import BaseModel, Field
from models.mongo import ObjectIdStr
from models.datetime import DateTime


class Post(BaseModel):
    content: str
    creation_time: DateTime
    modification_time: DateTime
    author: ObjectIdStr


class PostInit(BaseModel):
    content: str
    author: ObjectIdStr


class PostPatch(BaseModel):
    content: str


class PostId(BaseModel):
    post_id: ObjectIdStr


class PostWithId(Post):
    id: Annotated[ObjectIdStr, Field(validation_alias='_id')]


class PostNotFound(BaseModel):
    message: str = "Post not found"


class PostsList(BaseModel):
    posts: list[PostWithId]
