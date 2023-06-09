from flask_cors import CORS


def init(app) -> None:
    ORIGINS = ["*"]
    CORS(app, origins=ORIGINS)
