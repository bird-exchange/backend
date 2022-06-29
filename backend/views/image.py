from http import HTTPStatus

from flask import Blueprint, jsonify

from backend import schemas
from backend.repos.images import ImageRepo

view = Blueprint('images', __name__)
image_repo = ImageRepo()


@view.post('/')
def add_image():
    pass


@view.get('/')
def get_all_image():
    entities = image_repo.get_all()
    images = [schemas.Image.from_orm(entity).dict() for entity in entities]
    return jsonify(images), HTTPStatus.OK


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
