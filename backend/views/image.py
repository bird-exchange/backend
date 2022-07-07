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
def get_by_id_image(uid: int):
    entity = image_repo.get_by_id(uid)
    image = schemas.Image.from_orm(entity)
    return image.dict(), HTTPStatus.OK


@view.delete('/')
def delete_all_image():
    image_repo.delete_all()
    return {}, HTTPStatus.NO_CONTENT


@view.delete('/<uid>')
def delete_by_id_image(uid: int):
    image_repo.delete_by_id(uid)
    return {}, HTTPStatus.NO_CONTENT


@view.put('/<uid>')
def update_image():
    pass
