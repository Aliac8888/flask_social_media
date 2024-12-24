from flask import redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_openapi3.openapi import OpenAPI
from plugins import *
from routes import user_routes, post_routes, comment_routes
from config import be_host, be_port, jwt_secret, jwt_expiry
from flask_bcrypt import Bcrypt

app = OpenAPI(
    __name__,
    security_schemes={
        "jwt": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    },
)

app.config["JWT_SECRET_KEY"] = jwt_secret
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_expiry

bcrypt.init_app(app)
cors.init_app(app)
jwt.init_app(app)


@app.get("/", responses={302: None}, doc_ui=False)
def redirect_to_openapi():
    return redirect("/openapi")


# Register blueprints
app.register_api(user_routes.bp)
app.register_api(post_routes.bp)
app.register_api(comment_routes.bp)

if __name__ == "__main__":
    app.run(be_host, be_port, debug=True)
