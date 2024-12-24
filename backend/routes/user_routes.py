from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from models.user import *
from db import DUPLICATE_KEY, get_one, db
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId


users_tag = Tag(name="users")
followings_tag = Tag(name="followings")
bp = APIBlueprint("user", __name__, url_prefix="/users")


@bp.get("/", tags=[users_tag, followings_tag], responses={200: UsersList})
def list_users(query: UsersQuery):
    if query.following_id is None:
        users = db.users.find({}).to_list()
    else:
        users = db.users.find(
            {"followings": ObjectId(query.following_id)},
        ).to_list()

    return UsersList(users=users).model_dump()


@bp.post(
    "/",
    tags=[users_tag],
    responses={
        201: UserId,
        409: UserExists,
    },
)
def create_user(body: UserInit):
    try:
        result = db.users.insert_one(
            {"name": body.name, "email": body.email, "followings": []}
        )
    except OperationFailure as e:
        if e.code == DUPLICATE_KEY:
            return UserExists().model_dump(), 409

        raise

    return UserId(user_id=result.inserted_id).model_dump(), 201


@bp.get(
    "/<user_id>",
    tags=[users_tag],
    responses={
        200: User,
        404: UserNotFound,
    },
)
def get_user(path: UserId):
    i = db.users.find_one({"_id": ObjectId(path.user_id)})

    if i is None:
        return UserNotFound().model_dump(), 404

    return User.model_validate(i).model_dump()


@bp.patch(
    "/<user_id>",
    tags=[users_tag],
    responses={204: None, 404: UserNotFound, 409: UserExists},
)
def update_user(path: UserId, body: UserPatch):
    try:
        result = db.users.update_one(
            {"_id": ObjectId(path.user_id)},
            {"$set": body.model_dump(exclude_none=True)},
        )
    except OperationFailure as e:
        if e.code == DUPLICATE_KEY:
            return UserExists().model_dump(), 409

        raise

    if result.matched_count < 1:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.delete("/<user_id>", tags=[users_tag], responses={204: None, 404: UserNotFound})
def delete_user(path: UserId):
    result = db.users.delete_one({"_id": ObjectId(path.user_id)})

    if result.deleted_count < 1:
        return UserNotFound().model_dump(), 404

    db.users.update_many(
        {"followings": ObjectId(path.user_id)},
        {"$pull": {"followings": ObjectId(path.user_id)}},
    )

    posts = db.posts.find(
        {"author": ObjectId(path.user_id)},
        {"_id": 1},
    ).to_list()

    if posts:
        db.comments.delete_many({"post": {"$in": [i["_id"] for i in posts]}})

    db.posts.delete_many({"author": ObjectId(path.user_id)})
    db.comments.delete_many({"author": ObjectId(path.user_id)})

    return "", 204


@bp.get(
    "/<user_id>/followings",
    tags=[followings_tag],
    responses={200: UsersList, 404: UserNotFound},
)
def get_user_following(path: UserId):
    follower = db.users.find_one({"_id": ObjectId(path.user_id)})

    if follower is None:
        return UserNotFound().model_dump(), 404

    followings = db.users.find({"_id": {"$in": follower["followings"]}}).to_list()

    return UsersList(users=followings).model_dump()


@bp.put(
    "/<follower_id>/followings/<following_id>",
    tags=[followings_tag],
    responses={204: None, 404: UserNotFound},
)
def follow_user(path: Following):
    following = db.users.find_one({"_id": ObjectId(path.following_id)})

    if following is None:
        return UserNotFound().model_dump(), 404

    result = db.users.update_one(
        {"_id": ObjectId(path.follower_id)},
        {"$addToSet": {"followings": ObjectId(path.following_id)}},
    )

    if result.matched_count < 1:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<follower_id>/followings/<following_id>",
    tags=[followings_tag],
    responses={204: None, 404: UserNotFound},
)
def unfollow_user(path: Following):
    following = db.users.find_one({"_id": ObjectId(path.following_id)})

    if following is None:
        return UserNotFound().model_dump(), 404

    result = db.users.update_one(
        {"_id": ObjectId(path.follower_id)},
        {"$pull": {"followings": ObjectId(path.following_id)}},
    )

    if result.matched_count < 1:
        return UserNotFound().model_dump(), 404

    return "", 204
