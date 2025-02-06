"""Posts API."""

from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from server.auth.view_model import AuthnFailed, AuthzFailed
from server.model_utils import model_convert
from server.plugins import current_user
from server.posts.controller import (
    create_post,
    delete_post,
    get_all_posts,
    get_post_by_id,
    get_post_feed,
    get_posts_by_author,
    update_post,
)
from server.posts.controller_model import DbPostNotFoundError
from server.posts.view_model import (
    Post,
    PostId,
    PostInit,
    PostNotFound,
    PostPatch,
    PostsList,
)
from server.users.controller_model import DbUserNotFoundError
from server.users.view_model import UserId, UserNotFound

_posts_tag = Tag(name="posts")
bp = APIBlueprint("post", __name__, url_prefix="/posts")
"""Posts route blueprint."""


@bp.get("/", operation_id="getAllPosts", tags=[_posts_tag], responses={200: PostsList})
def handle_get_all_posts():  # noqa: ANN201
    """Get all posts."""
    posts = get_all_posts()

    return model_convert(PostsList, posts).model_dump()


@bp.get(
    "/by/<user_id>",
    operation_id="getPostsByAuthor",
    tags=[_posts_tag],
    responses={200: PostsList},
)
def handle_get_posts_by_author(path: UserId):  # noqa: ANN201
    """Get posts by an author."""
    posts = get_posts_by_author(path.user_id)

    return model_convert(PostsList, posts).model_dump()


@bp.get(
    "/feed/<user_id>",
    operation_id="getPostFeed",
    tags=[_posts_tag],
    security=[{"jwt": []}],
    responses={
        200: PostsList,
        401: AuthnFailed,
        403: AuthzFailed,
        404: UserNotFound,
    },
)
@jwt_required()
def handle_get_post_feed(path: UserId):  # noqa: ANN201
    """Get post feed of user."""
    if current_user.user_id != path.user_id and not current_user.admin:
        return AuthzFailed().model_dump(), 403

    try:
        posts = get_post_feed(path.user_id)
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404

    return model_convert(PostsList, posts).model_dump()


@bp.post(
    "/",
    operation_id="createPost",
    tags=[_posts_tag],
    security=[{"jwt": []}],
    responses={201: Post, 401: AuthnFailed, 403: AuthzFailed, 404: UserNotFound},
)
@jwt_required()
def handle_create_post(body: PostInit):  # noqa: ANN201
    """Create a post."""
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
    tags=[_posts_tag],
    responses={200: Post, 404: PostNotFound},
)
def handle_get_post_by_id(path: PostId):  # noqa: ANN201
    """Get post by ID."""
    try:
        post = get_post_by_id(path.post_id)
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return Post.model_validate(post).model_dump()


@bp.patch(
    "/<post_id>",
    operation_id="updatePost",
    tags=[_posts_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: PostNotFound},
)
@jwt_required()
def handle_update_post(path: PostId, body: PostPatch):  # noqa: ANN201
    """Update post."""
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
    tags=[_posts_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: PostNotFound},
)
@jwt_required()
def handle_delete_post(path: PostId):  # noqa: ANN201
    """Delete post."""
    try:
        delete_post(
            path.post_id,
            author_id=None if current_user.admin else current_user.user_id,
        )
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return "", 204
