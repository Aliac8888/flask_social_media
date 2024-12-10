from flask import Blueprint, request, jsonify
from db import db

bp = Blueprint("user", __name__, url_prefix="/users")

@bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    user = {
        "name": data["name"],
        "email": data["email"],
        "friends": []
    }
    db.users.insert_one(user)
    return jsonify({"message": "User created"}), 201
