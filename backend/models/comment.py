from pydantic import BaseModel
from models.mongo import ObjectIdStr


class Comment(BaseModel):
    content: str
    author: ObjectIdStr
    post: ObjectIdStr


class CommentInit(BaseModel):
    content: str
    author: ObjectIdStr
    post: ObjectIdStr


class CommentPatch(BaseModel):
    content: str


class CommentId(BaseModel):
    comment_id: ObjectIdStr


class CommentWithId(Comment):
    id: ObjectIdStr


class CommentNotFound(BaseModel):
    message: str = "Comment not found"


class CommentsList(BaseModel):
    comments: list[CommentWithId]
