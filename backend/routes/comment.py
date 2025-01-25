import datetime

from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from models.api.auth import AuthFailed
from models.api.comment import (
    Comment,
    CommentId,
    CommentInit,
    CommentNotFound,
    CommentPatch,
    CommentsList,
)
from models.api.post import PostId
from server.db import db, get_one
from server.plugins import current_user

comments_tag = Tag(name="comments")
bp = APIBlueprint("comment", __name__, url_prefix="/comments")


@bp.get("/", tags=[comments_tag], responses={200: CommentsList})
def handle_comments_get(query: PostId):  # noqa: ANN201
    comments = db.comments.aggregate(
        [
            {"$match": {"post": ObjectId(query.post_id)}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                },
            },
            {"$unwind": {"path": "$author"}},
        ],
    ).to_list()

    return CommentsList(comments).model_dump()


@bp.post(
    "/",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={201: CommentId, 403: AuthFailed},
)
@jwt_required()
def handle_comments_post(body: CommentInit):  # noqa: ANN201
    if current_user.user_id != body.author and not current_user.admin:
        return AuthFailed().model_dump(), 403

    now = datetime.datetime.now(datetime.UTC)

    result = db.comments.insert_one(
        {
            "content": body.content,
            "author": ObjectId(body.author),
            "post": ObjectId(body.post),
            "creation_time": now,
            "modification_time": now,
        },
    )

    return CommentId(comment_id=result.inserted_id).model_dump(), 201


@bp.get(
    "/<comment_id>",
    tags=[comments_tag],
    responses={200: Comment, 404: CommentNotFound},
)
def handle_comments_id_get(path: CommentId):  # noqa: ANN201
    i = get_one(
        db.comments.aggregate(
            [
                {"$match": {"_id": ObjectId(path.comment_id)}},
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "author",
                        "foreignField": "_id",
                        "as": "author",
                    },
                },
                {"$unwind": {"path": "$author"}},
            ],
        ),
    )

    if i is None:
        return CommentNotFound().model_dump(), 404

    return Comment.model_validate(i).model_dump()


@bp.patch(
    "/<comment_id>",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 404: CommentNotFound},
)
@jwt_required()
def handle_comments_id_patch(path: CommentId, body: CommentPatch):  # noqa: ANN201
    now = datetime.datetime.now(datetime.UTC)
    comment_filter = {"_id": ObjectId(path.comment_id)}

    if not current_user.admin:
        comment_filter["author"] = ObjectId(current_user.user_id)

    result = db.comments.update_one(
        comment_filter,
        {
            "$set": {
                **body.model_dump(exclude_none=True),
                "modification_time": now,
            },
        },
    )

    if result.matched_count < 1:
        return CommentNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<comment_id>",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 404: CommentNotFound},
)
@jwt_required()
def handle_comments_id_delete(path: CommentId):  # noqa: ANN201
    comment_filter = {"_id": ObjectId(path.comment_id)}

    if not current_user.admin:
        comment_filter["author"] = ObjectId(current_user.user_id)

    result = db.comments.delete_one(comment_filter)

    if result.deleted_count < 1:
        return CommentNotFound().model_dump(), 404

    return "", 204
