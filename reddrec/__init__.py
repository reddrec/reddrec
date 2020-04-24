from flask import Flask
import reddrec.routes as routes
from reddrec.data_deps import DataDeps

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
        DataDeps.setup(app.config['datadeps'])
    else:
        DataDeps.setup()

    app.register_blueprint(routes.bp)

    return app
