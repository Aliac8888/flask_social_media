from flask import redirect
from flask_openapi3.openapi import OpenAPI
from routes import user_routes, post_routes, comment_routes
from config import be_host, be_port

app = OpenAPI(__name__)


@app.get("/", responses={302: None}, doc_ui=False)
def redirect_to_openapi():
    return redirect("/openapi")


# Register blueprints
app.register_api(user_routes.bp)
app.register_api(post_routes.bp)
app.register_api(comment_routes.bp)

if __name__ == "__main__":
    app.run(be_host, be_port, debug=True)
