from flask import Flask
from routes import user_routes, post_routes, comment_routes
from db import client

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_routes.bp)
app.register_blueprint(post_routes.bp)
app.register_blueprint(comment_routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
