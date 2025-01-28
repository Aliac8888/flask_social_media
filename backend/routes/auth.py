from flask_jwt_extended import create_access_token, jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from controllers.auth import change_password, login, signup
from models import model_convert
from models.api.auth import AuthFailed, AuthRequest, AuthResponse, UserPassword
from models.api.user import (
    User,
    UserExists,
    UserId,
    UserInit,
    UserNotFound,
)
from models.db.auth import AuthFailedError
from models.db.user import DbUserExistsError, DbUserNotFoundError
from server.config import admin_email, maintenance
from server.plugins import current_user

auth_tag = Tag(name="authentication")
bp = APIBlueprint("auth", __name__, url_prefix="/users")


@bp.post(
    "/signup",
    tags=[auth_tag],
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

    try:
        user = signup(
            name=body.name,
            email=body.email,
            password=body.password,
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
    if not body.password and not maintenance:
        return AuthFailed().model_dump(), 403

    try:
        user = login(body.email, body.password)
    except (DbUserNotFoundError, AuthFailedError):
        return AuthFailed().model_dump(), 403

    user = model_convert(User, user)

    return AuthResponse(
        user=user,
        jwt=create_access_token(user),
    ).model_dump()


@bp.put(
    "/<user_id>/password",
    tags=[auth_tag],
    security=[{"jwt": []}],
    responses={
        204: None,
        403: AuthFailed,
        404: UserNotFound,
    },
)
@jwt_required()
def handle_users_id_password_put(path: UserId, body: UserPassword):  # noqa: ANN201
    if current_user.admin and current_user.user_id == path.user_id:
        return AuthFailed().model_dump(), 403

    if not current_user.admin and current_user.user_id != path.user_id:
        return AuthFailed().model_dump(), 403

    if body.root == "" and not maintenance:
        return AuthFailed().model_dump(), 403

    try:
        change_password(
            path.user_id,
            password=body.root,
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204
