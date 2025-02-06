"""Controller for posts."""

from datetime import UTC, datetime

from bson.objectid import ObjectId

from server.db import db, get_one
from server.posts.controller_model import DbPost, DbPostList, DbPostNotFoundError


def get_all_posts() -> DbPostList:
    """Get all posts.

    Returns:
        DbPostList: Posts.

    """
    result = db.posts.aggregate(
        [
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

    return DbPostList.model_validate(result)


def get_post_by_id(post_id: ObjectId) -> DbPost:
    """Get post by ID.

    Args:
        post_id (ObjectId): ID of post.

    Raises:
        DbPostNotFoundError: No post with given ID exists.

    Returns:
        DbPost: The post.

    """
    result = get_one(
        db.posts.aggregate(
            [
                {"$match": {"_id": post_id}},
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
        )
    )

    if result is None:
        raise DbPostNotFoundError

    return DbPost.model_validate(result)


def validate_post_id(post_id: ObjectId) -> None:
    """Check if a post with the given ID exists without fetching its data.

    Args:
        post_id (ObjectId): Id of post.

    Raises:
        DbPostNotFoundError: No post with the given ID exists.

    """
    result = db.posts.find_one({"_id": post_id}, {"_id": 1})

    if result is None:
        raise DbPostNotFoundError


def get_posts_by_author(author_id: ObjectId) -> DbPostList:
    """Get posts by an author.

    Args:
        author_id (ObjectId): Id of authoring user.

    Returns:
        DbPostList: Posts by the author.

    """
    result = db.posts.aggregate(
        [
            {"$match": {"author": author_id}},
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

    return DbPostList.model_validate(result)


def get_post_feed(user_id: ObjectId) -> DbPostList:
    """Get post feed of user.

    Args:
        user_id (ObjectId): Id of user.

    Raises:
        DbUserNotFoundError: User with the given ID was not in the database.

    Returns:
        DbPostList: Posts in user's feed.

    """
    from server.users.controller import get_user_by_id

    user = get_user_by_id(user_id)

    result = db.posts.aggregate(
        [
            {"$match": {"author": {"$in": [user_id, *user.followings]}}},
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

    return DbPostList.model_validate(result)


def create_post(
    content: str,
    author_id: ObjectId,
) -> DbPost:
    """Create a post.

    Args:
        content (str): Post content.
        author_id (ObjectId): Author of the post.

    Raises:
        DbUserNotFoundError: User with the given ID was not in the database.

    Returns:
        DbPost: Created post.

    """
    from server.users.controller import get_user_by_id

    now = datetime.now(UTC)
    user = get_user_by_id(author_id)

    post = {
        "content": content,
        "creation_time": now,
        "modification_time": now,
        "author": author_id,
    }

    result = db.posts.insert_one(post)

    post["_id"] = result.inserted_id
    post["author"] = user

    return DbPost.model_validate(post)


def update_post(
    post_id: ObjectId,
    content: str,
    author_id: ObjectId | None = None,
) -> None:
    """Update post.

    Args:
        post_id (ObjectId): Id of post.
        content (str): New content.
        author_id (ObjectId, optional): Expected post author. Defaults to None,
            which allows any author.

    Raises:
        DbPostNotFoundError: No post with the given ID and author was found.

    """
    now = datetime.now(UTC)
    post_filter = {"_id": post_id}

    if author_id is not None:
        post_filter["author"] = author_id

    result = db.posts.update_one(
        post_filter,
        {
            "$set": {
                "content": content,
                "modification_time": now,
            },
        },
    )

    if result.matched_count < 1:
        raise DbPostNotFoundError


def delete_post(post_id: ObjectId, author_id: ObjectId | None = None) -> None:
    """Delete post.

    Args:
        post_id (ObjectId): Id of post.
        author_id (ObjectId, optional): Expected post author. Defaults to None,
            which allows any author.

    Raises:
        DbPostNotFoundError: No post with the given ID and author was found.

    """
    from server.comments.controller import delete_comments_of_post

    post_filter = {"_id": post_id}

    if author_id is not None:
        post_filter["author"] = author_id

    result = db.posts.delete_one(post_filter)

    if result.deleted_count < 1:
        raise DbPostNotFoundError

    delete_comments_of_post(post_id)


def delete_posts_by_author(author_id: ObjectId) -> bool:
    """Delete all posts by author.

    Args:
        author_id (ObjectId): ID of authoring user.

    Returns:
        bool: was anything deleted?

    """
    from server.comments.controller import delete_comments_of_many_posts

    posts = db.posts.find({"author": author_id}, {"_id": 1}).to_list()

    delete_comments_of_many_posts([i["_id"] for i in posts])

    result = db.posts.delete_many({"author": author_id})

    return result.deleted_count > 0
