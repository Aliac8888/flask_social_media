from typing import Any, cast

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import current_user as _current_user

from server.auth.view_model import (
    AuthnExpired,
    AuthnIdentity,
    AuthnInvalid,
    AuthnMissing,
)
from server.config import admin_email, fe_url
from server.users.view_model import User

bcrypt = Bcrypt()
cors = CORS(origins=fe_url)
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity(user: User) -> str:
    return AuthnIdentity(
        user_id=user.id,
        admin=user.email == admin_email,
    ).model_dump_json()


@jwt.user_lookup_loader
def user_lookup(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> AuthnIdentity:
    return AuthnIdentity.model_validate_json(jwt_data["sub"])


@jwt.expired_token_loader
def expired_token(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    return AuthnExpired(details="expired").model_dump(), 401


@jwt.invalid_token_loader
def invalid_token(error_string: str):  # noqa: ANN201
    return AuthnInvalid(details=error_string).model_dump(), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    return AuthnExpired(details="gone stale").model_dump(), 401


@jwt.revoked_token_loader
def revoked_token(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    return AuthnExpired(details="revoked").model_dump(), 401


@jwt.token_verification_failed_loader
def token_verification_failed(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    return AuthnInvalid(details="verification failed").model_dump(), 401


@jwt.unauthorized_loader
def unauthorized(error_string: str):  # noqa: ANN201
    return AuthnMissing(details=error_string).model_dump(), 401


@jwt.user_lookup_error_loader
def user_lookup_error(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    return AuthnInvalid(details="lookup failed").model_dump(), 401


current_user = cast(AuthnIdentity, _current_user)
