"""User Followings API."""

from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from server.auth.view_model import AuthnFailed, AuthzFailed
from server.followings.controller import (
    follow_user,
    get_user_followers,
    get_user_followings,
    unfollow_user,
)
from server.followings.view_model import Following
from server.model_utils import model_convert
from server.plugins import current_user
from server.users.controller_model import DbUserNotFoundError
from server.users.view_model import UserId, UserNotFound, UsersList

_followings_tag = Tag(name="followings")
bp = APIBlueprint("following", __name__, url_prefix="/users")
"""User followings route blueprint."""


@bp.get(
    "/<user_id>/followers",
    operation_id="getUserFollowers",
    tags=[_followings_tag],
    responses={200: UsersList},
)
def handle_get_user_followers(path: UserId):  # noqa: ANN201
    """Get user followers."""
    followers = get_user_followers(path.user_id)

    return model_convert(UsersList, followers).model_dump()


@bp.get(
    "/<user_id>/followings",
    operation_id="getUserFollowings",
    tags=[_followings_tag],
    responses={200: UsersList, 404: UserNotFound},
)
def handle_get_user_followings(path: UserId):  # noqa: ANN201
    """Get user followings."""
    try:
        followings = get_user_followings(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(UsersList, followings).model_dump()


@bp.put(
    "/<follower_id>/followings/<following_id>",
    operation_id="followUser",
    tags=[_followings_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 403: AuthzFailed, 404: UserNotFound},
)
@jwt_required()
def handle_follow_user(path: Following):  # noqa: ANN201
    """Follow user."""
    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthzFailed().model_dump(), 403

    try:
        follow_user(path.follower_id, path.following_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<follower_id>/followings/<following_id>",
    operation_id="unfollowUser",
    tags=[_followings_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 403: AuthzFailed, 404: UserNotFound},
)
@jwt_required()
def handle_unfollow_user(path: Following):  # noqa: ANN201
    """Unfollow user."""
    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthzFailed().model_dump(), 403

    try:
        unfollow_user(path.follower_id, path.following_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204
