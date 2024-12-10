from flask import Blueprint, request, jsonify
from db import db
from bson import ObjectId
import datetime

bp = Blueprint("comment", __name__, url_prefix="/comments")

@bp.route("/post/<post_id>", methods=["GET"])
def get_comments(post_id):
    comments = list(db.comments.find({"post_id": ObjectId(post_id)}, {"_id": 0}))
    return jsonify(comments), 200
 
 
@bp.route("/", methods=["POST"])
def create_comment():
    data = request.json
    comment = {
        "content": data["content"],
        "author": ObjectId(data["author"]),
        "post_id": ObjectId(data["post_id"])
    }
    db.comments.insert_one(comment)
    return jsonify({"message": "Comment created"}), 201


@bp.route("/<comment_id>", methods=["PUT"])
def update_comment(comment_id):
    data = request.json
    db.comments.update_one({"_id": ObjectId(comment_id)}, {"$set": data})
    return jsonify({"message": "Comment updated"}), 200


@bp.route("/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    db.comments.delete_one({"_id": ObjectId(comment_id)})
    return jsonify({"message": "Comment deleted"}), 200
