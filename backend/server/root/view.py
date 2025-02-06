"""API Root."""

from flask import redirect
from flask_openapi3.blueprint import APIBlueprint

import server.auth.view
import server.comments.view
import server.followings.view
import server.posts.view
import server.users.view

bp = APIBlueprint("root", __name__, url_prefix="/")
"""Root blueprint."""

bp.register_api(server.auth.view.bp)
bp.register_api(server.users.view.bp)
bp.register_api(server.followings.view.bp)
bp.register_api(server.posts.view.bp)
bp.register_api(server.comments.view.bp)


@bp.get("/", responses={302: None}, doc_ui=False)
def handle_root_get():  # noqa: ANN201
    """Redirect to a OpenAPI viewer."""
    return redirect("/openapi")
