"""Controller for Users."""

from bson.objectid import ObjectId
from pydantic import validate_email
from pymongo.errors import OperationFailure

from server.config import admin_email
from server.db import DUPLICATE_KEY, db
from server.users.controller_model import (
    DbUser,
    DbUserExistsError,
    DbUserList,
    DbUserNotFoundError,
)


def get_all_users() -> DbUserList:
    """Get all users.

    Returns:
        DbUserList: Users in the database.

    """
    result = db.users.find({}).to_list()

    return DbUserList.model_validate(result)


def get_user_by_id(user_id: ObjectId) -> DbUser:
    """Get user by ID.

    Args:
        user_id (ObjectId): ID of user.

    Raises:
        DbUserNotFoundError: User with the given ID was not in the database.

    Returns:
        DbUser: The user in the database.

    """
    result = db.users.find_one({"_id": user_id})

    if result is None:
        raise DbUserNotFoundError

    return DbUser.model_validate(result)


def validate_user_id(user_id: ObjectId) -> None:
    """Verify that a user by the given ID exists without retrieving their data.

    Args:
        user_id (ObjectId): ID of user.

    Raises:
        DbUserNotFoundError: User with the given ID was not in the database.

    """
    result = db.users.find_one({"_id": user_id}, {"_id": 1})

    if result is None:
        raise DbUserNotFoundError


def get_user_by_email(email: str) -> DbUser:
    """Get user by email address.

    Args:
        email (str): Email address of user.

    Raises:
        DbUserNotFoundError: User with the given email was not in the database.

    Returns:
        DbUser: The user in the database.

    """
    result = db.users.find_one({"email": email})

    if result is None:
        raise DbUserNotFoundError

    return result and DbUser.model_validate(result)


def create_user(
    name: str,
    email: str,
    credential: bytes,
) -> DbUser:
    """Create a user.

    Do not use this directly. This function requires a hashed credential.
    Use the `server.auth.controller.signup` function instead, which accepts
    a password as input.

    Args:
        name (str): Name of user.
        email (str): Email address of user.
        credential (bytes): Hashed credential of user.

    Raises:
        DbUserExistsError: User with given email address already exists.

    Returns:
        DbUser: Created user.

    """
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
) -> bool:
    """Update user.

    Do not use the `credential` parameter directly.
    Use `server.auth.controller.change_password` instead.

    Args:
        user_id (ObjectId): Id of user.
        name (str, optional): New name of user. Defaults to None.
        email (str, optional): New email of user. Defaults to None.
        credential (bytes, optional): New credential of user. Defaults to None.

    Raises:
        DbUserExistsError: Given email address is already used.
        DbUserNotFoundError: No user with the given id exist.

    """
    patch = {}

    if name is not None:
        patch["name"] = name

    if email is not None:
        validate_email(email)
        patch["email"] = email

    if credential is not None:
        patch["credential"] = credential

    if not patch:
        return False

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

    return result.modified_count > 0


def delete_user(user_id: ObjectId) -> None:
    """Delete user.

    Args:
        user_id (ObjectId): Id of user.

    Raises:
        DbUserNotFoundError: No user with the given Id exists.

    """
    from server.comments.controller import delete_comments_by_author
    from server.posts.controller import delete_posts_by_author

    result = db.users.delete_one(
        {"_id": user_id, "email": {"$ne": {"$literal": admin_email}}},
    )

    if result.deleted_count < 1:
        raise DbUserNotFoundError

    db.users.update_many({"followings": user_id}, {"$pull": {"followings": user_id}})

    delete_posts_by_author(user_id)
    delete_comments_by_author(user_id)
