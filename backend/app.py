from flask_openapi3.openapi import OpenAPI

import plugins
from config import jwt_expiry, jwt_secret
from routes import bp


def create_app() -> OpenAPI:
    app = OpenAPI(
        __name__,
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
