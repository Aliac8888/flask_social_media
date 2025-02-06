"""Authentication/Authorization API."""

from flask_jwt_extended import create_access_token, jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from server.auth.controller import change_password, login, signup
from server.auth.controller_model import AuthnFailedError
from server.auth.view_model import (
    AuthnFailed,
    AuthnRequest,
    AuthnResponse,
    AuthzFailed,
    UserPassword,
)
from server.config import admin_email, maintenance
from server.model_utils import model_convert
from server.plugins import current_user
from server.users.controller_model import DbUserExistsError, DbUserNotFoundError
from server.users.view_model import User, UserExists, UserId, UserInit, UserNotFound

_auth_tag = Tag(name="auth")
bp = APIBlueprint("auth", __name__, url_prefix="/users")
"""Authentication/Authorization route blueprint."""


@bp.post(
    "/signup",
    operation_id="signup",
    tags=[_auth_tag],
    responses={
        201: AuthnResponse,
        403: AuthzFailed,
        409: UserExists,
    },
)
def handle_signup(body: UserInit):  # noqa: ANN201
    """Signup."""
    if body.email == admin_email and not maintenance:
        return UserExists().model_dump(), 409

    if not body.password and not maintenance:
        return AuthzFailed().model_dump(), 403

    try:
        user = signup(
            name=body.name,
            email=body.email,
            password=body.password,
        )
    except DbUserExistsError:
        return UserExists().model_dump(), 409

    user = model_convert(User, user)

    return AuthnResponse(
        user=user,
        jwt=create_access_token(user),
    ).model_dump()


@bp.post(
    "/login",
    operation_id="login",
    tags=[_auth_tag],
    responses={200: AuthnResponse, 403: AuthzFailed},
)
def handle_login(body: AuthnRequest):  # noqa: ANN201
    """Login."""
    if not body.password and not maintenance:
        return AuthzFailed().model_dump(), 403

    try:
        user = login(body.email, body.password)
    except (DbUserNotFoundError, AuthnFailedError):
        return AuthzFailed().model_dump(), 403

    user = model_convert(User, user)

    return AuthnResponse(
        user=user,
        jwt=create_access_token(user),
    ).model_dump()


@bp.put(
    "/<user_id>/password",
    operation_id="changePassword",
    tags=[_auth_tag],
    security=[{"jwt": []}],
    responses={
        204: None,
        401: AuthnFailed,
        403: AuthzFailed,
        404: UserNotFound,
    },
)
@jwt_required()
def handle_change_password(path: UserId, body: UserPassword):  # noqa: ANN201
    """Change user password."""
    if current_user.admin and current_user.user_id == path.user_id:
        return AuthzFailed().model_dump(), 403

    if not current_user.admin and current_user.user_id != path.user_id:
        return AuthzFailed().model_dump(), 403

    if body.root == "" and not maintenance:
        return AuthzFailed().model_dump(), 403

    try:
        change_password(
            path.user_id,
            password=body.root,
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204
