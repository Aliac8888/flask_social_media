from flask_jwt_extended import create_access_token, jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from controllers.auth import change_password, login, signup
from models import model_convert
from models.api.auth import (
    AuthnFailed,
    AuthnRequest,
    AuthnResponse,
    AuthzFailed,
    UserPassword,
)
from models.api.user import (
    User,
    UserExists,
    UserId,
    UserInit,
    UserNotFound,
)
from models.db.auth import AuthnFailedError
from models.db.user import DbUserExistsError, DbUserNotFoundError
from server.config import admin_email, maintenance
from server.plugins import current_user

auth_tag = Tag(name="authentication")
bp = APIBlueprint("auth", __name__, url_prefix="/users")


@bp.post(
    "/signup",
    operation_id="signup",
    tags=[auth_tag],
    responses={
        201: AuthnResponse,
        403: AuthzFailed,
        409: UserExists,
    },
)
def handle_signup(body: UserInit):  # noqa: ANN201
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
    tags=[auth_tag],
    responses={200: AuthnResponse, 403: AuthzFailed},
)
def handle_login(body: AuthnRequest):  # noqa: ANN201
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
    tags=[auth_tag],
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
