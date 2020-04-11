from flask import Flask
import reddrec.routes as routes

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(routes.bp)
    return app
