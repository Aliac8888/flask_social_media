import datetime
from flask_jwt_extended import current_user, jwt_required
from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from models.auth import JwtIdentity, AuthFailed
from models.post import PostId
from models.comment import *
from db import db, get_one
from bson.objectid import ObjectId

comments_tag = Tag(name="comments")
bp = APIBlueprint("comment", __name__, url_prefix="/comments")


@bp.get("/", tags=[comments_tag], responses={200: CommentsList})
def get_comments(query: PostId):
    comments = db.comments.aggregate(
        [
            {"$match": {"post": ObjectId(query.post_id)}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                }
            },
            {"$unwind": {"path": "$author"}},
        ]
    ).to_list()

    return CommentsList(comments=comments).model_dump()


@bp.post(
    "/",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={201: CommentId, 403: AuthFailed},
)
@jwt_required()
def create_comment(body: CommentInit):
    assert isinstance(current_user, JwtIdentity)

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
        }
    )

    return CommentId(comment_id=result.inserted_id).model_dump(), 201


@bp.get(
    "/<comment_id>", tags=[comments_tag], responses={200: Comment, 404: CommentNotFound}
)
def get_comment(path: CommentId):
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
                    }
                },
                {"$unwind": {"path": "$author"}},
            ]
        )
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
def update_comment(path: CommentId, body: CommentPatch):
    assert isinstance(current_user, JwtIdentity)
    now = datetime.datetime.now(datetime.UTC)
    filter = {"_id": ObjectId(path.comment_id)}

    if not current_user.admin:
        filter["author"] = ObjectId(current_user.user_id)

    result = db.comments.update_one(
        filter,
        {
            "$set": {
                **body.model_dump(exclude_none=True),
                "modification_time": now,
            }
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
def delete_comment(path: CommentId):
    assert isinstance(current_user, JwtIdentity)
    filter = {"_id": ObjectId(path.comment_id)}

    if not current_user.admin:
        filter["author"] = ObjectId(current_user.user_id)

    result = db.comments.delete_one(filter)

    if result.deleted_count < 1:
        return CommentNotFound().model_dump(), 404

    return "", 204
