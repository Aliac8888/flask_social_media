from typing import Any, cast

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_current_user
from werkzeug.local import LocalProxy

from models.api.auth import JwtIdentity
from models.api.user import User
from server.config import admin_email, fe_url

bcrypt = Bcrypt()
cors = CORS(origins=fe_url)
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity(user: User) -> str:
    return JwtIdentity(
        user_id=user.id,
        admin=user.email == admin_email,
    ).model_dump_json()


@jwt.user_lookup_loader
def user_lookup(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> JwtIdentity:
    return JwtIdentity.model_validate_json(jwt_data["sub"])


current_user = cast(JwtIdentity, LocalProxy[JwtIdentity](lambda: get_current_user()))
