from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from models.post import PostId
from models.comment import *
from db import db
from bson import ObjectId

comments_tag = Tag(name="comments")
bp = APIBlueprint("comment", __name__, url_prefix="/comments")


@bp.get("/", tags=[comments_tag], responses={200: CommentsList})
def get_comments(query: PostId):
    comments = db.comments.find({"post": ObjectId(query.post_id)})

    return CommentsList(
        comments=[CommentWithId(**i, id=i["_id"]) for i in comments]
    ).model_dump()


@bp.post("/", tags=[comments_tag], responses={201: CommentId})
def create_comment(body: CommentInit):
    result = db.comments.insert_one(
        {
            "content": body.content,
            "author": ObjectId(body.author),
            "post": ObjectId(body.post),
        }
    )

    return CommentId(comment_id=result.inserted_id).model_dump(), 201


@bp.patch(
    "/<comment_id>", tags=[comments_tag], responses={204: None, 404: CommentNotFound}
)
def update_comment(path: CommentId, body: CommentPatch):
    result = db.comments.update_one(
        {"_id": ObjectId(path.comment_id)},
        {"$set": body.model_dump(exclude_none=True)},
    )

    if result.matched_count < 1:
        return CommentNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<comment_id>", tags=[comments_tag], responses={204: None, 404: CommentNotFound}
)
def delete_comment(comment_id):
    result = db.comments.delete_one({"_id": ObjectId(comment_id)})

    if result.deleted_count < 1:
        return CommentNotFound().model_dump(), 404

    return "", 204
