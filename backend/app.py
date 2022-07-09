from http import HTTPStatus

from flask import Flask
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from backend.config import config
from backend.db import create_all, db_session
from backend.errors import AppError
from backend.views import image, task, upload


def handle_http_exceptions(error: HTTPException):
    return {'message': error.description}, error.code


def handle_app_error(error: AppError):
    return {'message': error.reason}, error.status


def handle_validation_error(error: ValidationError):
    return error.json(), HTTPStatus.BAD_REQUEST


def shutdown_session(exception=None):
    db_session.remove()


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE_URL=config.db.url,
        APP_PORT=config.server.port,
        APP_HOST=config.server.host
    )

    create_all()

    app.register_blueprint(image.view, url_prefix='/api/v1/image')
    app.register_blueprint(task.view, url_prefix='/api/v1/task')
    app.register_blueprint(upload.view, url_prefix='/api/v1/upload')
    app.register_error_handler(HTTPException, handle_http_exceptions)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(ValidationError, handle_validation_error)

    app.teardown_appcontext(shutdown_session)

    return app
