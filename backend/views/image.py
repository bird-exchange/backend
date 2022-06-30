from http import HTTPStatus

from flask import Blueprint, jsonify, request

from backend import schemas
from backend.repos.images import ImageRepo

view = Blueprint('images', __name__)
image_repo = ImageRepo()


@view.post('/')
def add_image():
    image_data = request.json
    image_data['uid'] = -1
    image_data = schemas.Image(**image_data)

    entity = image_repo.add_image(image_data.name, image_data.type)
    new_image = schemas.Image.from_orm(entity)

    return new_image.dict(), HTTPStatus.CREATED


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
