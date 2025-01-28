from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from controllers.following import (
    follow_user,
    get_user_followers,
    get_user_followings,
    unfollow_user,
)
from models import model_convert
from models.api.auth import AuthFailed
from models.api.following import Following
from models.api.user import (
    UserId,
    UserNotFound,
    UsersList,
)
from models.db.user import DbUserNotFoundError
from server.plugins import current_user

followings_tag = Tag(name="followings")
bp = APIBlueprint("following", __name__, url_prefix="/users")


@bp.get(
    "/<user_id>/followers",
    operation_id="getUserFollowers",
    tags=[followings_tag],
    responses={200: UsersList, 404: UserNotFound},
)
def handle_get_user_followers(path: UserId):  # noqa: ANN201
    try:
        followers = get_user_followers(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(UsersList, followers).model_dump()


@bp.get(
    "/<user_id>/followings",
    operation_id="getUserFollowings",
    tags=[followings_tag],
    responses={200: UsersList, 404: UserNotFound},
)
def handle_get_user_followings(path: UserId):  # noqa: ANN201
    try:
        followings = get_user_followings(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(UsersList, followings).model_dump()


@bp.put(
    "/<follower_id>/followings/<following_id>",
    operation_id="followUser",
    tags=[followings_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def handle_follow_user(path: Following):  # noqa: ANN201
    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        follow_user(path.follower_id, path.following_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<follower_id>/followings/<following_id>",
    operation_id="unfollowUser",
    tags=[followings_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def handle_unfollow_user(path: Following):  # noqa: ANN201
    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        unfollow_user(path.follower_id, path.following_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204
