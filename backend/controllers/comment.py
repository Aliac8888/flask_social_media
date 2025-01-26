from datetime import UTC, datetime

from bson.objectid import ObjectId

from controllers.post import validate_post_id
from controllers.user import get_user_by_id
from models.database.comments import DbComment, DbCommentList, DbCommentNotFoundError
from server.db import db, get_one


def get_comment_by_id(comment_id: ObjectId) -> DbComment:
    result = get_one(
        db.comments.aggregate(
            [
                {"$match": {"_id": comment_id}},
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "author",
                        "foreignField": "_id",
                        "as": "author",
                    },
                },
                {"$unwind": {"path": "$author"}},
            ],
        ),
    )

    if result is None:
        raise DbCommentNotFoundError

    return DbComment.model_validate(result)


def validate_comment_id(comment_id: ObjectId) -> None:
    result = db.comments.find_one({"_id": comment_id}, {"_id": 1})

    if result is None:
        raise DbCommentNotFoundError


def get_comments_of_post(post_id: ObjectId) -> DbCommentList:
    result = db.comments.aggregate(
        [
            {"$match": {"post": post_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                },
            },
            {"$unwind": {"path": "$author"}},
        ],
    ).to_list()

    return DbCommentList.model_validate(result)


def create_comment(content: str, author_id: ObjectId, post_id: ObjectId) -> DbComment:
    now = datetime.now(UTC)
    author = get_user_by_id(author_id)
    validate_post_id(post_id)

    comment = {
        "content": content,
        "author": author_id,
        "post": post_id,
        "creation_time": now,
        "modification_time": now,
    }

    result = db.comments.insert_one(comment)

    comment["author"] = author
    comment["_id"] = result.inserted_id

    return DbComment.model_validate(comment)


def update_comment(
    comment_id: ObjectId, content: str, author_id: ObjectId | None = None
) -> None:
    now = datetime.now(UTC)
    comment_filter = {"_id": comment_id}

    if author_id is not None:
        comment_filter["author"] = author_id

    result = db.comments.update_one(
        comment_filter,
        {
            "$set": {
                "content": content,
                "modification_time": now,
            },
        },
    )

    if result.matched_count < 1:
        raise DbCommentNotFoundError


def delete_comment(comment_id: ObjectId, author_id: ObjectId | None = None) -> None:
    comment_filter = {"_id": comment_id}

    if author_id is not None:
        comment_filter["author"] = author_id

    result = db.comments.delete_one(comment_filter)

    if result.deleted_count < 1:
        raise DbCommentNotFoundError


def delete_comments_by_author(author_id: ObjectId) -> bool:
    result = db.comments.delete_many({"author": author_id})

    return result.deleted_count > 0


def delete_comments_of_post(post_id: ObjectId) -> bool:
    result = db.comments.delete_many({"post": post_id})

    return result.deleted_count > 0


def delete_comments_of_many_posts(post_ids: list[ObjectId]) -> bool:
    if not post_ids:
        return False

    result = db.comments.delete_many({"post": {"$in": post_ids}})

    return result.deleted_count > 0
