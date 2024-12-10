from flask import Blueprint, request, jsonify
from db import db
from bson import ObjectId
import datetime

bp = Blueprint("post", __name__, url_prefix="/posts")

@bp.route("/", methods=["GET"])
def get_posts():
    posts = list(db.posts.find({}, {"_id": 0}))
    return jsonify(posts), 200


@bp.route("/", methods=["POST"])
def create_post():
    data = request.json
    post = {
        "content": data["content"],
        "date": datetime.UTC,
        "author": ObjectId(data["author"])
    }
    db.posts.insert_one(post)
    return jsonify({"message": "Post created"}), 201


@bp.route("/<post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.json
    db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": data})
    return jsonify({"message": "Post updated"}), 200
