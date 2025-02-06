"""Controller of Comments."""

from datetime import UTC, datetime
from typing import Any

from bson.objectid import ObjectId

from server.comments.controller_model import (
    DbComment,
    DbCommentList,
    DbCommentNotFoundError,
)
from server.db import db, get_one


def get_comment_by_id(comment_id: ObjectId) -> DbComment:
    """Get comment by Id.

    Args:
        comment_id (ObjectId): Id of comment.

    Raises:
        DbCommentNotFoundError: No comment by the given Id was found.

    Returns:
        DbComment: Found Comment.

    """
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
    """Check if a comment id exists without retrieving its data.

    Args:
        comment_id (ObjectId): Id of comment.

    Raises:
        DbCommentNotFoundError: No comment with the given id exists.

    """
    result = db.comments.find_one({"_id": comment_id}, {"_id": 1})

    if result is None:
        raise DbCommentNotFoundError


def get_comments_of_post(post_id: ObjectId) -> DbCommentList:
    """Get comments of post.

    Args:
        post_id (ObjectId): Id of post.

    Returns:
        DbCommentList: Comments of post.

    """
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


def get_comments_by_author(author_id: ObjectId) -> DbCommentList:
    """Get comments by an author.

    Args:
        author_id (ObjectId): Id of authoring user.

    Raises:
        DbUserNotFoundError: User with the given ID was not in the database.

    Returns:
        DbCommentList: Comments of post.

    """
    from server.users.controller import get_user_by_id
    author = get_user_by_id(author_id)

    result = db.comments.find({"author": author_id}).to_list()

    for i in result:
        i["author"] = author

    return DbCommentList.model_validate(result)


def create_comment(content: str, author_id: ObjectId, post_id: ObjectId) -> DbComment:
    """Create a comment.

    Args:
        content (str): Content of comment.
        author_id (ObjectId): Id of authoring user.
        post_id (ObjectId): Id of post.

    Raises:
        DbPostNotFoundError: No post with the given ID exists.
        DbUserNotFoundError: User with the given ID was not in the database.

    Returns:
        DbComment: Created Comment.

    """
    from server.posts.controller import validate_post_id
    from server.users.controller import get_user_by_id

    now = datetime.now(UTC)
    author = get_user_by_id(author_id)
    validate_post_id(post_id)

    comment: dict[str, Any] = {
        "content": content,
        "author": author_id,
        "post": post_id,
        "creation_time": now,
        "modification_time": now,
    }

    result = db.comments.insert_one(comment)

    comment["author"] = author.model_dump()
    comment["_id"] = result.inserted_id

    return DbComment.model_validate(comment)


def update_comment(
    comment_id: ObjectId, content: str, author_id: ObjectId | None = None
) -> None:
    """Update a comment.

    Args:
        comment_id (ObjectId): Id of comment.
        content (str): New content
        author_id (ObjectId, optional): Expected comment author. Defaults to None,
            which allows any author.

    Raises:
        DbPostNotFoundError: No comment with the given ID and author was found.

    """
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
    """Delete a comment.

    Args:
        comment_id (ObjectId): Id of comment.
        author_id (ObjectId, optional): Expected comment author. Defaults to None,
            which allows any author.

    Raises:
        DbPostNotFoundError: No comment with the given ID and author was found.

    """
    comment_filter = {"_id": comment_id}

    if author_id is not None:
        comment_filter["author"] = author_id

    result = db.comments.delete_one(comment_filter)

    if result.deleted_count < 1:
        raise DbCommentNotFoundError


def delete_comments_by_author(author_id: ObjectId) -> bool:
    """Delete all comments by author.

    Args:
        author_id (ObjectId): Id of authoring user.

    Returns:
        bool: was anything deleted?

    """
    result = db.comments.delete_many({"author": author_id})

    return result.deleted_count > 0


def delete_comments_of_post(post_id: ObjectId) -> bool:
    """Delete all comments by post.

    Args:
        post_id (ObjectId): Id of post.

    Returns:
        bool: was anything deleted?

    """
    result = db.comments.delete_many({"post": post_id})

    return result.deleted_count > 0


def delete_comments_of_many_posts(post_ids: list[ObjectId]) -> bool:
    """Delete all comments by many posts.

    Args:
        post_ids (list[ObjectId]): Id of posts.

    Returns:
        bool: was anything deleted?

    """
    if not post_ids:
        return False

    result = db.comments.delete_many({"post": {"$in": post_ids}})

    return result.deleted_count > 0
