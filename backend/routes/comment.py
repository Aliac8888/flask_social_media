from flask_jwt_extended import jwt_required
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from pydantic import RootModel

from controllers.comment import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments_of_post,
    update_comment,
)
from models import model_convert
from models.api.auth import AuthnFailed, AuthzFailed
from models.api.comment import (
    Comment,
    CommentId,
    CommentInit,
    CommentNotFound,
    CommentPatch,
    CommentsList,
)
from models.api.post import PostId, PostNotFound
from models.api.user import UserNotFound
from models.db.comments import DbCommentNotFoundError
from models.db.post import DbPostNotFoundError
from models.db.user import DbUserNotFoundError
from server.plugins import current_user

comments_tag = Tag(name="comments")
bp = APIBlueprint("comment", __name__, url_prefix="/comments")


@bp.get(
    "/",
    operation_id="getCommentsOfPost",
    tags=[comments_tag],
    responses={200: CommentsList},
)
def handle_get_comments_of_post(query: PostId):  # noqa: ANN201
    comments = get_comments_of_post(query.post_id)

    return model_convert(CommentsList, comments).model_dump()


@bp.post(
    "/",
    operation_id="createComment",
    tags=[comments_tag],
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
    tags=[comments_tag],
    responses={200: Comment, 404: CommentNotFound},
)
def handle_get_comment_by_id(path: CommentId):  # noqa: ANN201
    try:
        comment = get_comment_by_id(path.comment_id)
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return model_convert(Comment, comment).model_dump()


@bp.patch(
    "/<comment_id>",
    operation_id="updateComment",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: CommentNotFound},
)
@jwt_required()
def handle_update_comment(path: CommentId, body: CommentPatch):  # noqa: ANN201
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
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 401: AuthnFailed, 404: CommentNotFound},
)
@jwt_required()
def handle_delete_comment(path: CommentId):  # noqa: ANN201
    try:
        delete_comment(
            path.comment_id,
            None if current_user.admin else current_user.user_id,
        )
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return "", 204
