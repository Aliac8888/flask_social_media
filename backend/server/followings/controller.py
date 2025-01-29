from bson.objectid import ObjectId

from server.db import db
from server.users.controller_model import DbUserList, DbUserNotFoundError


def get_user_followers(following_id: ObjectId) -> DbUserList:
    result = db.users.find(
        {"followings": following_id},
    ).to_list()

    return DbUserList.model_validate(result)


def get_user_followings(follower_id: ObjectId) -> DbUserList:
    from server.users.controller import get_user_by_id

    follower = get_user_by_id(follower_id)

    result = db.users.find({"_id": {"$in": follower.followings}}).to_list()

    return DbUserList.model_validate(result)


def follow_user(follower_id: ObjectId, following_id: ObjectId) -> bool:
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
    from server.users.controller import validate_user_id

    validate_user_id(following_id)

    result = db.users.update_one(
        {"_id": follower_id},
        {"$pull": {"followings": following_id}},
    )

    if result.matched_count < 1:
        raise DbUserNotFoundError

    return result.modified_count > 0
