from flask import Flask, jsonify, make_response
import reddrec.routes as routes

def create_app(config=None):
    app = Flask(__name__)
    app.register_blueprint(routes.bp)
    return app
