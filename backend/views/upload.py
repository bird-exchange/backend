from flask import Blueprint

view = Blueprint('upload', __name__)


@view.post('/')
def download_image():
    pass


@view.get('/<uid>')
def get_link_to_image():
    pass
