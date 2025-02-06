"""Comments API."""

from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from pydantic import RootModel

from server.auth.view_model import AuthnFailed, AuthzFailed
from server.comments.controller import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments_of_post,
    update_comment,
)
from server.comments.controller_model import DbCommentNotFoundError
from server.comments.view_model import (
    Comment,
    CommentId,
    CommentInit,
    CommentNotFound,
    CommentPatch,
    CommentsList,
)
from server.model_utils import model_convert
from server.plugins import current_user
from server.posts.controller_model import DbPostNotFoundError
from server.posts.view_model import PostId, PostNotFound
from server.users.controller_model import DbUserNotFoundError
from server.users.view_model import UserNotFound

_comments_tag = Tag(name="comments")
bp = APIBlueprint("comment", __name__, url_prefix="/comments")
"""Comments route blueprint."""


@bp.get(
    "/of/<post_id>",
    operation_id="getCommentsOfPost",
    tags=[_comments_tag],
    responses={200: CommentsList},
)
def handle_get_comments_of_post(path: PostId):  # noqa: ANN201
    """Get comments of post."""
    comments = get_comments_of_post(path.post_id)

    return model_convert(CommentsList, comments).model_dump()


@bp.post(
    "/",
    operation_id="createComment",
    tags=[_comments_tag],
    security=[{"jwt": []}],
    responses={
        201: CommentId,
        401: AuthnFailed,
        403: AuthzFailed,
        404: RootModel[UserNotFound | PostNotFound],
    },
)
@jwt_required()
def handle_create_comment(body: CommentInit):  # noqa: ANN201
    """Create a comment."""
    if current_user.user_id != body.author and not current_user.admin:
        return AuthzFailed().model_dump(), 403

    try:
        comment = create_comment(
            content=body.content,
            author_id=body.author,
            post_id=body.post,
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return model_convert(Comment, comment).model_dump(), 201


@bp.get(
    "/<comment_id>",
    operation_id="getCommentById",
    tags=[_comments_tag],
    responses={200: Comment, 404: CommentNotFound},
)
def handle_get_comment_by_id(path: CommentId):  # noqa: ANN201
    """Get a comment by ID."""
    try:
        comment = get_comment_by_id(path.comment_id)
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return model_convert(Comment, comment).model_dump()


@bp.patch(
    "/<comment_id>",
    operation_id="updateComment",
    tags=[_comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: CommentNotFound},
)
@jwt_required()
def handle_update_comment(path: CommentId, body: CommentPatch):  # noqa: ANN201
    """Update comment."""
    try:
        update_comment(
            path.comment_id,
            body.content,
            None if current_user.admin else current_user.user_id,
        )
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<comment_id>",
    operation_id="deleteComment",
    tags=[_comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: CommentNotFound},
)
@jwt_required()
def handle_delete_comment(path: CommentId):  # noqa: ANN201
    """Delete comment."""
    try:
        delete_comment(
            path.comment_id,
            None if current_user.admin else current_user.user_id,
        )
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return "", 204
