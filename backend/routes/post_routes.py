from flask_openapi3.models.tag import Tag
from flask_openapi3.blueprint import APIBlueprint
from models.post import *
from db import db
from bson import ObjectId
import datetime

posts_tag = Tag(name="posts")
bp = APIBlueprint("post", __name__, url_prefix="/posts")


@bp.get("/", tags=[posts_tag], responses={200: PostsList})
def list_posts():
    posts = db.posts.find({})

    return PostsList(posts=[PostWithId(**i, id=i["_id"]) for i in posts]).model_dump()


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


@bp.patch("/<post_id>", tags=[posts_tag], responses={204: None, 404: PostNotFound})
def update_post(path: PostId, body: PostPatch):
    result = db.posts.update_one(
        {"_id": ObjectId(path.post_id)},
        {"$set": body.model_dump(exclude_none=True)},
    )

    if result.matched_count < 1:
        return PostNotFound().model_dump(), 404

    return "", 204
