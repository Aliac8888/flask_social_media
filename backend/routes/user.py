from flask_jwt_extended import create_access_token, jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from controllers.user import (
    create_user,
    delete_user,
    follow_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    get_user_followers,
    get_user_followings,
    unfollow_user,
    update_user,
)
from models import model_convert
from models.api.auth import AuthFailed, AuthRequest, AuthResponse
from models.api.user import (
    Following,
    User,
    UserExists,
    UserId,
    UserInit,
    UserNotFound,
    UserPatch,
    UsersList,
    UsersQuery,
)
from models.db.user import DbUserExistsError, DbUserNotFoundError
from server.config import admin_email, maintenance
from server.plugins import bcrypt, current_user

users_tag = Tag(name="users")
followings_tag = Tag(name="followings")
auth_tag = Tag(name="authentication")
bp = APIBlueprint("user", __name__, url_prefix="/users")


@bp.get("/", tags=[users_tag, followings_tag], responses={200: UsersList})
def handle_users_get(query: UsersQuery):  # noqa: ANN201
    users = (
        get_all_users()
        if query.following_id is None
        else get_user_followers(query.following_id)
    )

    return model_convert(UsersList, users).model_dump()


@bp.post(
    "/",
    tags=[users_tag, auth_tag],
    responses={
        201: AuthResponse,
        403: AuthFailed,
        409: UserExists,
    },
)
def handle_users_post(body: UserInit):  # noqa: ANN201
    if body.email == admin_email and not maintenance:
        return UserExists().model_dump(), 409

    if not body.password and not maintenance:
        return AuthFailed().model_dump(), 403

    credential = bcrypt.generate_password_hash(body.password) if body.password else b""

    try:
        user = create_user(
            name=body.name,
            email=body.email,
            credential=credential,
        )
    except DbUserExistsError:
        return UserExists().model_dump(), 409

    user = model_convert(User, user)

    return AuthResponse(
        user=user,
        jwt=create_access_token(user),
    ).model_dump()


@bp.post(
    "/login",
    tags=[auth_tag],
    responses={200: AuthResponse, 403: AuthFailed},
)
def handle_users_login_post(body: AuthRequest):  # noqa: ANN201
    try:
        user = get_user_by_email(body.email)
    except DbUserNotFoundError:
        return AuthFailed().model_dump(), 403

    if not user.credential and not maintenance:
        return AuthFailed().model_dump(), 403

    if user.credential and not bcrypt.check_password_hash(
        user.credential,
        body.password,
    ):
        return AuthFailed().model_dump(), 403

    user = model_convert(User, user)

    return AuthResponse(
        user=user,
        jwt=create_access_token(user),
    ).model_dump()


@bp.get(
    "/<user_id>",
    tags=[users_tag],
    responses={
        200: User,
        404: UserNotFound,
    },
)
def handle_users_id_get(path: UserId):  # noqa: ANN201
    try:
        user = get_user_by_id(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(User, user).model_dump()


@bp.patch(
    "/<user_id>",
    tags=[users_tag],
    security=[{"jwt": []}],
    responses={
        204: None,
        403: AuthFailed,
        404: UserNotFound,
        409: UserExists,
    },
)
@jwt_required()
def handle_users_id_patch(path: UserId, body: UserPatch):  # noqa: ANN201
    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    credential = None

    if body.password is not None:
        if not body.password and not maintenance:
            return AuthFailed().model_dump(), 403

        credential = (
            bcrypt.generate_password_hash(body.password) if body.password else b""
        )

    try:
        update_user(
            path.user_id,
            name=body.name,
            email=body.email,
            credential=credential,
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404
    except DbUserExistsError:
        return UserExists().model_dump(), 409

    return "", 204


@bp.delete(
    "/<user_id>",
    tags=[users_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def handle_users_id_delete(path: UserId):  # noqa: ANN201
    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        delete_user(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.get(
    "/<user_id>/followings",
    tags=[followings_tag],
    responses={200: UsersList, 404: UserNotFound},
)
def handle_users_id_followings_get(path: UserId):  # noqa: ANN201
    try:
        followings = get_user_followings(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(UsersList, followings).model_dump()


@bp.put(
    "/<follower_id>/followings/<following_id>",
    tags=[followings_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def handle_users_id_followings_id_put(path: Following):  # noqa: ANN201
    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        follow_user(path.follower_id, path.following_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<follower_id>/followings/<following_id>",
    tags=[followings_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def handle_users_id_followings_id_delete(path: Following):  # noqa: ANN201
    if current_user.user_id != path.follower_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        unfollow_user(path.follower_id, path.following_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204
