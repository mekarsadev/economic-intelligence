import os

import click
from flask.cli import AppGroup

app_cli = AppGroup("system")


@app_cli.command("createapp")
@click.option(
    "--name", "-n", prompt="application name", help="Naming for application packages"
)
def generate_app(name, *agrs, **kwagrs):
    subdir = ["viewsets", "serializers", "models"]

    os.mkdir(os.path.join(os.getcwd(), "src", name))
    app_directory = os.path.join(os.getcwd(), "src", name)

    for item in subdir:
        os.mkdir(os.path.join(app_directory, item))
        os.system(f"touch {os.path.join(app_directory, item)}/__init__.py")
