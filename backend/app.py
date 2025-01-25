from flask import redirect
from flask_openapi3.openapi import OpenAPI

import plugins
from config import be_host, be_port, jwt_expiry, jwt_secret
from routes import comment, post, user

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


@app.get("/", responses={302: None}, doc_ui=False)
def redirect_to_openapi():  # noqa: ANN201
    return redirect("/openapi")


# Register blueprints
app.register_api(user.bp)
app.register_api(post.bp)
app.register_api(comment.bp)

if __name__ == "__main__":
    app.run(be_host, be_port, debug=True)
