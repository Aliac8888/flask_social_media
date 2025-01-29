from datetime import UTC, datetime

from bson.objectid import ObjectId

from server.db import db, get_one
from server.posts.controller_model import DbPost, DbPostList, DbPostNotFoundError


def get_all_posts() -> DbPostList:
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
    result = db.posts.find_one({"_id": post_id}, {"_id": 1})

    if result is None:
        raise DbPostNotFoundError


def get_posts_by_author(author_id: ObjectId) -> DbPostList:
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
    from server.comments.controller import delete_comments_of_post

    post_filter = {"_id": post_id}

    if author_id is not None:
        post_filter["author"] = author_id

    result = db.posts.delete_one(post_filter)

    if result.deleted_count < 1:
        raise DbPostNotFoundError

    delete_comments_of_post(post_id)


def delete_posts_by_author(author_id: ObjectId) -> bool:
    from server.comments.controller import delete_comments_of_many_posts

    posts = db.posts.find({"author": author_id}, {"_id": 1}).to_list()

    delete_comments_of_many_posts([i["_id"] for i in posts])

    result = db.posts.delete_many({"author": author_id})

    return result.deleted_count > 0
