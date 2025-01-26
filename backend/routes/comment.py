from bson.objectid import ObjectId
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
from models.api.auth import AuthFailed
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


@bp.get("/", tags=[comments_tag], responses={200: CommentsList})
def handle_comments_get(query: PostId):  # noqa: ANN201
    comments = get_comments_of_post(ObjectId(query.post_id))

    return model_convert(CommentsList, comments).model_dump()


@bp.post(
    "/",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={
        201: CommentId,
        403: AuthFailed,
        404: RootModel[UserNotFound | PostNotFound],
    },
)
@jwt_required()
def handle_comments_post(body: CommentInit):  # noqa: ANN201
    if current_user.user_id != body.author and not current_user.admin:
        return AuthFailed().model_dump(), 403

    try:
        comment = create_comment(
            content=body.content,
            author_id=ObjectId(body.author),
            post_id=ObjectId(body.post),
        )
    except DbUserNotFoundError:
        return UserNotFound().model_dump(), 404
    except DbPostNotFoundError:
        return PostNotFound().model_dump(), 404

    return model_convert(Comment, comment).model_dump(), 201


@bp.get(
    "/<comment_id>",
    tags=[comments_tag],
    responses={200: Comment, 404: CommentNotFound},
)
def handle_comments_id_get(path: CommentId):  # noqa: ANN201
    try:
        comment = get_comment_by_id(ObjectId(path.comment_id))
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return model_convert(Comment, comment).model_dump()


@bp.patch(
    "/<comment_id>",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 404: CommentNotFound},
)
@jwt_required()
def handle_comments_id_patch(path: CommentId, body: CommentPatch):  # noqa: ANN201
    try:
        update_comment(
            ObjectId(path.comment_id),
            body.content,
            None if current_user.admin else ObjectId(current_user.user_id),
        )
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return "", 204


@bp.delete(
    "/<comment_id>",
    tags=[comments_tag],
    security=[{"jwt": []}],
    responses={204: None, 404: CommentNotFound},
)
@jwt_required()
def handle_comments_id_delete(path: CommentId):  # noqa: ANN201
    try:
        delete_comment(
            ObjectId(path.comment_id),
            None if current_user.admin else ObjectId(current_user.user_id),
        )
    except DbCommentNotFoundError:
        return CommentNotFound().model_dump(), 404

    return "", 204
