from http import HTTPStatus

from flask import Blueprint, jsonify, request

from backend import schemas
from backend.config import config
from backend.repos.image import ImageRepo
from backend.repos.files import FilesRepo

view = Blueprint('images', __name__)
image_repo = ImageRepo()
file_repo = FilesRepo()

bucket_input = config.aws.bucket_input_images
bucket_output = config.aws.bucket_output_images


@view.post('/')
def add_image():
    image_data = request.json
    image_data['uid'] = -1
    image_data = schemas.Image(**image_data)

    entity = image_repo.add_image(**image_data.dict())
    new_image = schemas.Image.from_orm(entity)

    return new_image.dict(), HTTPStatus.CREATED


@view.get('/')
def get_all_image():
    kind = request.args.get('kind')

    if kind == 'sparrow':
        entities = image_repo.get_all_sparrow()
    elif kind == 'tit':
        entities = image_repo.get_all_tit()
    elif kind == 'all':
        entities = image_repo.get_all()
    else:
        raise ValueError

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
    file_repo.delete_all(bucket_input)
    file_repo.delete_all(bucket_output)
    return {}, HTTPStatus.NO_CONTENT


@view.delete('/<uid>')
def delete_by_id_image(uid: int):
    image = image_repo.get_by_id(uid)
    image_repo.delete_by_id(uid)
    file_repo.delete_file_by_name(bucket_input, image.name)
    file_repo.delete_file_by_name(bucket_output, image.name)
    return {}, HTTPStatus.NO_CONTENT


@view.put('/<uid>')
def update_by_id_image(uid):
    payload = request.json
    payload['uid'] = int(uid)
    image = schemas.Image(**payload)
    entity = image_repo.update_by_id(**image.dict())
    new_image = schemas.Image.from_orm(entity)
    return new_image.dict(), HTTPStatus.OK
