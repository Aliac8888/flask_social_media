"""Controller for User Followings."""

from bson.objectid import ObjectId

from server.db import db
from server.users.controller_model import DbUserList, DbUserNotFoundError


def get_user_followers(following_id: ObjectId) -> DbUserList:
    """Get user followers.

    Args:
        following_id (ObjectId): Id of user being followed.

    Returns:
        DbUserList: Followers.

    """
    result = db.users.find(
        {"followings": following_id},
    ).to_list()

    return DbUserList.model_validate(result)


def get_user_followings(follower_id: ObjectId) -> DbUserList:
    """Get user followings.

    Args:
        follower_id (ObjectId): Id of user who is following others.

    Raises:
        DbUserNotFoundError: User with the given ID was not in the database.

    Returns:
        DbUserList: Followings.

    """
    from server.users.controller import get_user_by_id

    follower = get_user_by_id(follower_id)

    result = db.users.find({"_id": {"$in": follower.followings}}).to_list()

    return DbUserList.model_validate(result)


def follow_user(follower_id: ObjectId, following_id: ObjectId) -> bool:
    """Follow user.

    Args:
        follower_id (ObjectId): Id of user who will be following the other.
        following_id (ObjectId): Id of user being followed.

    Raises:
        DbUserNotFoundError: At least one of the users were not found.

    Returns:
        bool: did anything change?

    """
    from server.users.controller import validate_user_id

    validate_user_id(following_id)

    result = db.users.update_one(
        {"_id": follower_id},
        {"$addToSet": {"followings": following_id}},
    )

    if result.matched_count < 1:
        raise DbUserNotFoundError

    return result.modified_count > 0


def unfollow_user(follower_id: ObjectId, following_id: ObjectId) -> bool:
    """Unfollow a user.

    Args:
        follower_id (ObjectId): Id of user who was following the other.
        following_id (ObjectId): Id of user being followed.

    Raises:
        DbUserNotFoundError: At least one of the users were not found.

    Returns:
        bool: did anything change?

    """
    from server.users.controller import validate_user_id

    validate_user_id(following_id)

    result = db.users.update_one(
        {"_id": follower_id},
        {"$pull": {"followings": following_id}},
    )

    if result.matched_count < 1:
        raise DbUserNotFoundError

    return result.modified_count > 0
