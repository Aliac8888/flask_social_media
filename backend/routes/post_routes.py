from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from backend.models.user import UserId, UserNotFound
from models.post import *
from db import db
from bson import ObjectId
import datetime
# mm
posts_tag = Tag(name="posts")
bp = APIBlueprint("post", __name__, url_prefix="/posts")


@bp.get("/", tags=[posts_tag], responses={200: PostsList})
def list_posts():
    posts = db.posts.find({}).to_list()
    return PostsList(posts=posts).model_dump()

@bp.get("/", tags=[posts_tag], responses={200: PostsList})
def get_posts(query: UserId):
    posts = db.posts.find({"author": {"$eq": ObjectId(query.user_id)}}).to_list()

    return PostsList(posts=posts).model_dump()


@bp.get(
    "/feed", tags=[posts_tag], responses={200: PostsList, 404: UserNotFound}
)
def get_feed(query: UserId):
    user = db.users.find_one({"_id": ObjectId(query.user_id)})

    if user is None:
        return UserNotFound().model_dump(), 404

    posts = db.posts.find({"author": {"$in": user["friends"]}}).to_list()

    return PostsList(posts=posts).model_dump()



@bp.post("/", tags=[posts_tag], responses={201: PostId})
def create_post(body: PostInit):
    now = datetime.datetime.now(datetime.UTC)

    result = db.posts.insert_one(
        {
            "content": body.content,
            "creation_time": now,
            "modification_time": now,
            "author": ObjectId(body.author),
        }
    )

    return PostId(post_id=result.inserted_id).model_dump(), 201


@bp.patch(
    "/<post_id>", tags=[posts_tag], responses={200: PostWithId, 404: PostNotFound}
)
def get_post(path: PostId):
    post = db.posts.find_one({"_id": path.post_id})

    if post is None:
        return PostNotFound().model_dump(), 404

    return PostWithId(**post).model_dump()


@bp.patch("/<post_id>", tags=[posts_tag], responses={204: None, 404: PostNotFound})
def update_post(path: PostId, body: PostPatch):
    now = datetime.datetime.now(datetime.UTC)

    result = db.posts.update_one(
        {"_id": ObjectId(path.post_id)},
        {
            "$set": {
                **body.model_dump(exclude_none=True),
                "modification_time": now,
            }
        },
    )

    if result.matched_count < 1:
        return PostNotFound().model_dump(), 404

    return "", 204


@bp.delete("/<post_id>", tags=[posts_tag], responses={204: None, 404: PostNotFound})
def delete_post(path: PostId):
    result = db.posts.delete_one({"_id": ObjectId(path.post_id)})

    if result.deleted_count < 1:
        return PostNotFound().model_dump(), 404

    db.comments.delete_many({"post": ObjectId(path.post_id)})

    return "", 204
