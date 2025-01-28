from flask import redirect
from flask_openapi3.blueprint import APIBlueprint

from routes import auth, comment, following, post, user

bp = APIBlueprint("root", __name__, url_prefix="/")

bp.register_api(auth.bp)
bp.register_api(user.bp)
bp.register_api(following.bp)
bp.register_api(post.bp)
bp.register_api(comment.bp)


@bp.get("/", responses={302: None}, doc_ui=False)
def handle_root_get():  # noqa: ANN201
    return redirect("/openapi")
