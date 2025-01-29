from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from controllers.post import (
    create_post,
    delete_post,
    get_all_posts,
    get_post_by_id,
    get_post_feed,
    get_posts_by_author,
    update_post,
)
from models import model_convert
from models.api.auth import AuthnFailed, AuthzFailed
from models.api.post import (
    Post,
    PostId,
    PostInit,
    PostNotFound,
    PostPatch,
    PostQuery,
    PostsList,
)
from models.api.user import UserId, UserNotFound
from models.db.post import DbPostNotFoundError
from models.db.user import DbUserNotFoundError
from server.plugins import current_user

posts_tag = Tag(name="posts")
bp = APIBlueprint("post", __name__, url_prefix="/posts")


@bp.get("/", operation_id="getAllPosts", tags=[posts_tag], responses={200: PostsList})
def handle_get_all_posts(query: PostQuery):  # noqa: ANN201
    posts = (
        get_all_posts()
        if query.author_id is None
        else get_posts_by_author(query.author_id)
    )

    return model_convert(PostsList, posts).model_dump()


@bp.get(
    "/feed",
    operation_id="getPostFeed",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={
        200: PostsList,
        401: AuthnFailed,
        403: AuthzFailed,
        404: UserNotFound,
    },
)
@jwt_required()
def handle_get_post_feed(query: UserId):  # noqa: ANN201
    if current_user.user_id != query.user_id and not current_user.admin:
        return AuthzFailed().model_dump(), 403

    try:
        posts = get_post_feed(query.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(PostsList, posts).model_dump()


@bp.post(
    "/",
    operation_id="createPost",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={201: Post, 401: AuthnFailed, 403: AuthzFailed, 404: UserNotFound},
)
@jwt_required()
def handle_create_post(body: PostInit):  # noqa: ANN201
    if current_user.user_id != body.author and not current_user.admin:
        return AuthzFailed().model_dump(), 403

    try:
        post = create_post(
            content=body.content,
            author_id=body.author,
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(Post, post).model_dump(), 201


@bp.get(
    "/<post_id>",
    operation_id="getPostById",
    tags=[posts_tag],
    responses={200: Post, 404: PostNotFound},
)
def handle_get_post_by_id(path: PostId):  # noqa: ANN201
    try:
        post = get_post_by_id(path.post_id)
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return Post.model_validate(post).model_dump()


@bp.patch(
    "/<post_id>",
    operation_id="updatePost",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: PostNotFound},
)
@jwt_required()
def handle_update_post(path: PostId, body: PostPatch):  # noqa: ANN201
    try:
        update_post(
            path.post_id,
            content=body.content,
            author_id=None if current_user.admin else current_user.user_id,
        )
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<post_id>",
    operation_id="deletePost",
    tags=[posts_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: PostNotFound},
)
@jwt_required()
def handle_delete_post(path: PostId):  # noqa: ANN201
    try:
        delete_post(
            path.post_id,
            author_id=None if current_user.admin else current_user.user_id,
        )
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return "", 204
