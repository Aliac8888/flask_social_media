"""Create a WSGI flask app to serve requests."""

from flask_openapi3.models.info import Info
from flask_openapi3.models.license import License
from flask_openapi3.openapi import OpenAPI

from server import plugins
from server.config import jwt_expiry, jwt_secret
from server.root.view import bp


def create_app() -> OpenAPI:
    """Create a flask app.

    Returns:
        OpenAPI: The flask app.

    """
    info = Info(
        title="Chamran Social",
        license=License(
            name="MIT",
            identifier="MIT",
        ),
        version="0.0",
    )

    app = OpenAPI(
        __name__,
        info=info,
        security_schemes={
            "jwt": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
        },
    )

    app.config["JWT_SECRET_KEY"] = jwt_secret
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_expiry

    plugins.bcrypt.init_app(app)
    plugins.cors.init_app(app)
    plugins.jwt.init_app(app)

    app.register_api(bp)

    return app
