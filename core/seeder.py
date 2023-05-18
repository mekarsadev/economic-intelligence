from flask import Flask

from seeder.skeleton import generate_app


def init(app: Flask) -> Flask:
    app.cli.add_command(generate_app)
