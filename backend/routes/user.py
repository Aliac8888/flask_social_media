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


@bp.get("/", tags=[users_tag], responses={200: UsersList})
def handle_users_get():  # noqa: ANN201
    users = get_all_users()

    return model_convert(UsersList, users).model_dump()


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
