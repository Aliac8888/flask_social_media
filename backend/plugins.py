from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models.auth import JwtIdentity
from db import db
from config import fe_url, admin_email
from bson.objectid import ObjectId

bcrypt = Bcrypt()
cors = CORS(origins=fe_url)
jwt = JWTManager()


@jwt.user_identity_loader
def user_identity(user):
    return JwtIdentity(
        user_id=user["_id"], admin=user["email"] == admin_email
    ).model_dump_json()


@jwt.user_lookup_loader
def user_lookup(_jwt_header, jwt_data):
    return JwtIdentity.model_validate_json(jwt_data["sub"])
