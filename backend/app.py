from flask import Flask
from backend.views import image, task, upload


def create_app():

    app = Flask(__name__)

    app.register_blueprint(image.view, url_prefix='/api/v1/image')
    app.register_blueprint(task.view, url_prefix='/api/v1/task')
    app.register_blueprint(upload.view, url_prefix='api/v1/upload')

    return app
