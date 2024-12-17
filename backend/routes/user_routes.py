from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from models.user import *
from db import DUPLICATE_KEY, db
from pymongo.errors import OperationFailure
from bson import ObjectId


users_tag = Tag(name="users")
bp = APIBlueprint("user", __name__, url_prefix="/users")


@bp.get("/", tags=[users_tag], responses={200: UsersList})
def list_users():
    users = db.users.find({}).to_list()
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
            {"name": body.name, "email": body.email, "friends": []}
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
        200: UserWithFriends,
        404: UserNotFound,
    },
)
def get_user(path: UserId):
    i = db.users.find_one({"_id": ObjectId(path.user_id)})

    if i is None:
        return UserNotFound().model_dump(), 404

    return UserWithFriends(**i).model_dump()


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


@bp.delete("/<user_id>", tags=[users_tag], responses={204: None})
def delete_user(path: UserId):
    result = db.users.delete_one({"_id": ObjectId(path.user_id)})

    if result.deleted_count < 1:
        return UserNotFound().model_dump(), 404

    return "", 204
