from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from models.user import *
from models.auth import *
from db import DUPLICATE_KEY, get_one, db
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId
from plugins import bcrypt
from config import admin_email, maintenance


users_tag = Tag(name="users")
followings_tag = Tag(name="followings")
auth_tag = Tag(name="authentication")
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
    tags=[users_tag, auth_tag],
    responses={
        201: AuthResponse,
        403: AuthFailed,
        409: UserExists,
    },
)
def create_user(body: UserInit):
    if body.email == admin_email and not maintenance:
        return UserExists().model_dump(), 409

    if not body.password and not maintenance:
        return AuthFailed().model_dump(), 403

    credential = bcrypt.generate_password_hash(body.password) if body.password else b""

    try:
        result = db.users.insert_one(
            {
                "name": body.name,
                "email": body.email,
                "credential": credential,
                "followings": [],
            }
        )
    except OperationFailure as e:
        if e.code == DUPLICATE_KEY:
            return UserExists().model_dump(), 409

        raise

    user = db.users.find_one({"_id": result.inserted_id})
    assert user is not None

    return AuthResponse(user=user, jwt=create_access_token(user)).model_dump()


@bp.post("/login", tags=[auth_tag], responses={200: AuthResponse, 403: AuthFailed})
def login(body: AuthRequest):
    user = db.users.find_one({"email": body.email})

    if user is None:
        return AuthFailed().model_dump(), 403

    if not user["credential"] and not maintenance:
        return AuthFailed().model_dump(), 403

    if user["credential"] and not bcrypt.check_password_hash(
        user["credential"], body.password
    ):
        return AuthFailed().model_dump(), 403

    return AuthResponse(user=user, jwt=create_access_token(user)).model_dump()


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
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound, 409: UserExists},
)
@jwt_required()
def update_user(path: UserId, body: UserPatch):
    assert isinstance(current_user, JwtIdentity)

    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    patch = body.model_dump(exclude_none=True)

    if "password" in patch:
        if not patch["password"] and not maintenance:
            return AuthFailed().model_dump(), 403

        patch["credential"] = (
            bcrypt.generate_password_hash(patch["password"])
            if patch["password"]
            else b""
        )

        del patch["password"]

    try:
        result = db.users.update_one(
            {
                "_id": ObjectId(path.user_id),
                "email": {"$ne": {"$literal": admin_email}},
            },
            {"$set": patch},
        )
    except OperationFailure as e:
        if e.code == DUPLICATE_KEY:
            return UserExists().model_dump(), 409

        raise

    if result.matched_count < 1:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<user_id>",
    tags=[users_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def delete_user(path: UserId):
    assert isinstance(current_user, JwtIdentity)

    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    result = db.users.delete_one(
        {"_id": ObjectId(path.user_id), "email": {"$ne": {"$literal": admin_email}}}
    )

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
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def follow_user(path: Following):
    assert isinstance(current_user, JwtIdentity)

    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

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
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def unfollow_user(path: Following):
    assert isinstance(current_user, JwtIdentity)

    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

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
