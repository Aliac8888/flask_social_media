import datetime

from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from models.api.auth import AuthFailed
from models.api.post import (
    Post,
    PostId,
    PostInit,
    PostNotFound,
    PostPatch,
    PostQuery,
    PostsList,
)
from models.api.user import UserId, UserNotFound
from server.db import db, get_one
from server.plugins import current_user

posts_tag = Tag(name="posts")
bp = APIBlueprint("post", __name__, url_prefix="/posts")


@bp.get("/", tags=[posts_tag], responses={200: PostsList})
def handle_posts_get(query: PostQuery):  # noqa: ANN201
    post_filter = (
        {} if query.author_id is None else {"author": ObjectId(query.author_id)}
    )

    posts = db.posts.aggregate(
        [
            {"$match": post_filter},
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

    return PostsList(posts).model_dump()


@bp.get(
    "/feed",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={
        200: PostsList,
        403: AuthFailed,
        404: UserNotFound,
    },
)
@jwt_required()
def handle_posts_feed_get(query: UserId):  # noqa: ANN201
    if current_user.user_id != query.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    user = db.users.find_one({"_id": ObjectId(query.user_id)})

    if user is None:
        return UserNotFound().model_dump(), 404

    posts = db.posts.aggregate(
        [
            {"$match": {"author": {"$in": [user["_id"], *user["followings"]]}}},
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

    return PostsList(posts).model_dump()


@bp.post(
    "/",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={201: PostId, 403: AuthFailed},
)
@jwt_required()
def handle_posts_post(body: PostInit):  # noqa: ANN201
    if current_user.user_id != body.author and not current_user.admin:
        return AuthFailed().model_dump(), 403

    now = datetime.datetime.now(datetime.UTC)

    result = db.posts.insert_one(
        {
            "content": body.content,
            "creation_time": now,
            "modification_time": now,
            "author": ObjectId(body.author),
        },
    )

    return PostId(post_id=result.inserted_id).model_dump(), 201


@bp.get(
    "/<post_id>",
    tags=[posts_tag],
    responses={200: Post, 404: PostNotFound},
)
def handle_posts_id_get(path: PostId):  # noqa: ANN201
    post = get_one(
        db.posts.aggregate(
            [
                {"$match": {"_id": ObjectId(path.post_id)}},
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

    if post is None:
        return PostNotFound().model_dump(), 404

    return Post.model_validate(post).model_dump()


@bp.patch(
    "/<post_id>",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={204: None, 404: PostNotFound},
)
@jwt_required()
def handle_posts_id_patch(path: PostId, body: PostPatch):  # noqa: ANN201
    now = datetime.datetime.now(datetime.UTC)
    post_filter = {"_id": ObjectId(path.post_id)}

    if not current_user.admin:
        post_filter["author"] = ObjectId(current_user.user_id)

    result = db.posts.update_one(
        post_filter,
        {
            "$set": {
                **body.model_dump(exclude_none=True),
                "modification_time": now,
            },
        },
    )

    if result.matched_count < 1:
        return PostNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<post_id>",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={204: None, 404: PostNotFound},
)
@jwt_required()
def handle_posts_id_delete(path: PostId):  # noqa: ANN201
    post_filter = {"_id": ObjectId(path.post_id)}

    if not current_user.admin:
        post_filter["author"] = ObjectId(current_user.user_id)

    result = db.posts.delete_one(post_filter)

    if result.deleted_count < 1:
        return PostNotFound().model_dump(), 404

    db.comments.delete_many({"post": ObjectId(path.post_id)})

    return "", 204
