from http import HTTPStatus

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from backend.config import get_config
from backend.db import init_db
from backend.errors import AppError
from backend.views import image, task, upload


def handle_http_exceptions(error: HTTPException):
    return {'message': error.description}, error.code


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


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

    app.register_error_handler(HTTPException, handle_http_exceptions)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    return app
