from flask_cors import CORS


def init(app) -> None:
    ORIGINS = ["*"]

    CORS.init_app(app, origins=ORIGINS)
