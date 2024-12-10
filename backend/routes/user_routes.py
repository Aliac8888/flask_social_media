from flask import Blueprint, request, jsonify
from db import db
from bson import ObjectId

bp = Blueprint("user", __name__, url_prefix="/users")

@bp.route("/", methods=["GET"])
def get_users():
    users = list(db.users.find({}, {"_id": 0}))
    return jsonify(users), 200


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


@bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    return jsonify({"message": "User updated"}), 200


@bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    db.users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "User deleted"}), 200
