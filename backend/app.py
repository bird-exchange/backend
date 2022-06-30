from flask import Flask

from backend.config import get_config
from backend.db import init_db
from backend.views import image, task, upload


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    config = get_config(test_config=test_config)

    app.config.from_mapping(
        DATABASE_URL=config.db.url,
        APP_PORT=config.server.port,
        APP_HOST=config.server.host
    )

    with app.app_context():
        init_db()

    app.register_blueprint(image.view, url_prefix='/api/v1/image')
    app.register_blueprint(task.view, url_prefix='/api/v1/task')
    app.register_blueprint(upload.view, url_prefix='/api/v1/upload')

    return app
