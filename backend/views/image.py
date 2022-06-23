from flask import Blueprint

view = Blueprint('images', __name__)


@view.post('/')
def add_image():
    pass


@view.get('/')
def get_all_image():
    pass


@view.get('/<uid>')
def get_image(uid: int):
    pass


@view.delete('/')
def delete_all_image():
    pass


@view.delete('/<uid>')
def delete_image(uid: int):
    pass


@view.put('/<uid>')
def update_image():
    pass
