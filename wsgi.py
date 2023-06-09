import os

from src import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=os.environ.get("FLASK_HOST", "localhost"),
        port=os.environ.get("FLASK_HOST", 5050),
    )
else:
    app = create_app()
