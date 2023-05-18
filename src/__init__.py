import os

from flask import Flask

from core.seeder import init as init_cli

from . import urls as api


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", None)

    api.init(app)
    init_cli(app)

    return app
