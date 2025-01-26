from bson.objectid import ObjectId
from pydantic import validate_email
from pymongo.errors import OperationFailure

from models.db.user import (
    DbUser,
    DbUserExistsError,
    DbUserList,
    DbUserNotFoundError,
)
from server.config import admin_email
from server.db import DUPLICATE_KEY, db


def get_all_users() -> DbUserList:
    result = db.users.find({}).to_list()

    return DbUserList.model_validate(result)


def get_user_by_id(user_id: ObjectId) -> DbUser:
    result = db.users.find_one({"_id": user_id})

    if result is None:
        raise DbUserNotFoundError

    return DbUser.model_validate(result)


def validate_user_id(user_id: ObjectId) -> None:
    result = db.users.find_one({"_id": user_id}, {"_id": 1})

    if result is None:
        raise DbUserNotFoundError


def get_user_by_email(email: str) -> DbUser:
    result = db.users.find_one({"email": email})

    if result is None:
        raise DbUserNotFoundError

    return result and DbUser.model_validate(result)


def get_user_followers(following_id: ObjectId) -> DbUserList:
    result = db.users.find(
        {"followings": ObjectId(following_id)},
    ).to_list()

    return DbUserList.model_validate(result)


def get_user_followings(follower_id: ObjectId) -> DbUserList:
    follower = get_user_by_id(follower_id)

    result = db.users.find({"_id": {"$in": follower.followings}}).to_list()

    return DbUserList.model_validate(result)


def create_user(
    name: str,
    email: str,
    credential: bytes,
) -> DbUser:
    validate_email(email)

    user = {
        "name": name,
        "email": email,
        "credential": credential,
        "followings": [],
    }

    try:
        result = db.users.insert_one(user)
    except OperationFailure as e:
        if e.code == DUPLICATE_KEY:
            raise DbUserExistsError from e

        raise

    user["_id"] = result.inserted_id

    return DbUser.model_validate(user)


def update_user(
    user_id: ObjectId,
    name: str | None = None,
    email: str | None = None,
    credential: bytes | None = None,
) -> None:
    patch = {}

    if name is not None:
        patch["name"] = name

    if email is not None:
        validate_email(email)
        patch["email"] = email

    if credential is not None:
        patch["credential"] = credential

    try:
        result = db.users.update_one(
            {
                "_id": user_id,
                "email": {"$ne": {"$literal": admin_email}},
            },
            {"$set": patch},
        )
    except OperationFailure as e:
        if e.code == DUPLICATE_KEY:
            raise DbUserExistsError from e

        raise

    if result.matched_count < 1:
        raise DbUserNotFoundError


def delete_user(user_id: ObjectId) -> None:
    from controllers.comment import delete_comments_by_author
    from controllers.post import delete_posts_by_author

    result = db.users.delete_one(
        {"_id": user_id, "email": {"$ne": {"$literal": admin_email}}},
    )

    if result.deleted_count < 1:
        raise DbUserNotFoundError

    db.users.update_many({"followings": user_id}, {"$pull": {"followings": user_id}})

    delete_posts_by_author(user_id)
    delete_comments_by_author(user_id)


def follow_user(follower_id: ObjectId, following_id: ObjectId) -> bool:
    validate_user_id(following_id)

    result = db.users.update_one(
        {"_id": follower_id},
        {"$addToSet": {"followings": following_id}},
    )

    if result.matched_count < 1:
        raise DbUserNotFoundError

    return result.modified_count > 0


def unfollow_user(follower_id: ObjectId, following_id: ObjectId) -> bool:
    validate_user_id(following_id)

    result = db.users.update_one(
        {"_id": follower_id},
        {"$pull": {"followings": following_id}},
    )

    if result.matched_count < 1:
        raise DbUserNotFoundError

    return result.modified_count > 0
