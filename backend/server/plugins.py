"""Flask server plugins/extensions."""

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
"""Bcrypt extension, for hashing and verifying passwords."""

cors = CORS(origins=fe_url)
"""Cross-Origin Resource Sharing extension, to allow frontend to access the API."""

jwt = JWTManager()
"""JWT extension, to manage authentication tokens."""


@jwt.user_identity_loader
def user_identity(user: User) -> str:
    """Create a new authentication identity of a user.

    Args:
        user (User): User data.

    Returns:
        str: JSON representation of an authentication identity.

    """
    return AuthnIdentity(
        user_id=user.id,
        admin=user.email == admin_email,
    ).model_dump_json()


@jwt.user_lookup_loader
def user_lookup(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> AuthnIdentity:
    """Load an authentication identity from JWT data.

    Args:
        _jwt_header (dict[str, Any]): JWT header.
        jwt_data (dict[str, Any]): JWT body.

    Returns:
        AuthnIdentity: The parsed jwt identity.

    """
    return AuthnIdentity.model_validate_json(jwt_data["sub"])


@jwt.expired_token_loader
def expired_token(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    """Expired token."""
    return AuthnExpired(details="expired").model_dump(), 401


@jwt.invalid_token_loader
def invalid_token(error_string: str):  # noqa: ANN201
    """Invalid token."""
    return AuthnInvalid(details=error_string).model_dump(), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    """Needs fresh token."""
    return AuthnExpired(details="gone stale").model_dump(), 401


@jwt.revoked_token_loader
def revoked_token(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    """Revoked token."""
    return AuthnExpired(details="revoked").model_dump(), 401


@jwt.token_verification_failed_loader
def token_verification_failed(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    """Token verification failed."""
    return AuthnInvalid(details="verification failed").model_dump(), 401


@jwt.unauthorized_loader
def unauthorized(error_string: str):  # noqa: ANN201
    """Unauthorized."""
    return AuthnMissing(details=error_string).model_dump(), 401


@jwt.user_lookup_error_loader
def user_lookup_error(_jwt_header: dict[str, Any], _jwt_data: dict[str, Any]):  # noqa: ANN201
    """User lookup error."""
    return AuthnInvalid(details="lookup failed").model_dump(), 401


current_user = cast(AuthnIdentity, _current_user)
"""Current authenticated user.

May be None if not using `@jwt_required` or if `optional=True`.
"""
