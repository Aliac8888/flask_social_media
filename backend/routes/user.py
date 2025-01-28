from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from controllers.user import (
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)
from models import model_convert
from models.api.auth import AuthFailed
from models.api.user import (
    User,
    UserExists,
    UserId,
    UserNotFound,
    UserPatch,
    UsersList,
)
from models.db.user import DbUserExistsError, DbUserNotFoundError
from server.plugins import current_user

users_tag = Tag(name="users")
bp = APIBlueprint("user", __name__, url_prefix="/users")


@bp.get("/", operation_id="getAllUsers", tags=[users_tag], responses={200: UsersList})
def handle_get_all_users():  # noqa: ANN201
    users = get_all_users()

    return model_convert(UsersList, users).model_dump()


@bp.get(
    "/me",
    operation_id="getCurrentUser",
    tags=[users_tag],
    security=[{}, {"jwt": []}],
    responses={
        200: User,
        404: UserNotFound,
    },
)
@jwt_required(optional=True)
def handle_get_current_user():  # noqa: ANN201
    if not current_user:
        return UserNotFound().model_dump(), 404

    try:
        user = get_user_by_id(current_user.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(User, user).model_dump()


@bp.get(
    "/<user_id>",
    operation_id="getUserById",
    tags=[users_tag],
    responses={
        200: User,
        404: UserNotFound,
    },
)
def handle_get_user_by_id(path: UserId):  # noqa: ANN201
    try:
        user = get_user_by_id(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(User, user).model_dump()


@bp.patch(
    "/<user_id>",
    operation_id="updateUser",
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
def handle_update_user(path: UserId, body: UserPatch):  # noqa: ANN201
    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        update_user(
            path.user_id,
            name=body.name,
            email=body.email,
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404
    except DbUserExistsError:
        return UserExists().model_dump(), 409

    return "", 204


@bp.delete(
    "/<user_id>",
    operation_id="deleteUser",
    tags=[users_tag],
    security=[{"jwt": []}],
    responses={204: None, 403: AuthFailed, 404: UserNotFound},
)
@jwt_required()
def handle_delete_user(path: UserId):  # noqa: ANN201
    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        delete_user(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return "", 204
