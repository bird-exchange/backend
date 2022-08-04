from http import HTTPStatus

from flask import Blueprint, jsonify, request

from backend import schemas
from backend.config import config
from backend.repos.bird import BirdRepo
from backend.repos.files import FilesRepo

view = Blueprint('birds', __name__)
bird_repo = BirdRepo()
file_repo = FilesRepo()

bucket_input = config.aws.bucket_input_images
bucket_output = config.aws.bucket_output_images


@view.post('/')
def add_bird():
    bird_data = request.json
    bird_data['uid'] = -1
    bird_data = schemas.Bird(**bird_data)

    entity = bird_repo.add_bird(**bird_data.dict())
    new_bird = schemas.Bird.from_orm(entity)

    return new_bird.dict(), HTTPStatus.CREATED


@view.get('/')
def get_all_bird():
    kind = request.args.get('kind')

    if kind == 'sparrow':
        entities = bird_repo.get_all_sparrow()
    elif kind == 'tit':
        entities = bird_repo.get_all_tit()
    elif kind == 'all':
        entities = bird_repo.get_all()
    else:
        raise ValueError

    birds = [schemas.Bird.from_orm(entity).dict() for entity in entities]
    return jsonify(birds), HTTPStatus.OK


@view.get('/<uid>')
def get_by_id_bird(uid: int):
    entity = bird_repo.get_by_id(uid)
    bird = schemas.Bird.from_orm(entity)
    return bird.dict(), HTTPStatus.OK


@view.delete('/')
def delete_all_bird():
    bird_repo.delete_all()
    file_repo.delete_all(bucket_input)
    file_repo.delete_all(bucket_output)
    return {}, HTTPStatus.NO_CONTENT


@view.delete('/<uid>')
def delete_by_id_bird(uid: int):
    bird = bird_repo.get_by_id(uid)
    bird_repo.delete_by_id(uid)
    file_repo.delete_file_by_name(bucket_input, bird.name)
    file_repo.delete_file_by_name(bucket_output, bird.name)
    return {}, HTTPStatus.NO_CONTENT


@view.put('/<uid>')
def update_by_id_bird(uid):
    payload = request.json
    payload['uid'] = int(uid)
    bird = schemas.Bird(**payload)
    entity = bird_repo.update_by_id(**bird.dict())
    new_bird = schemas.Bird.from_orm(entity)
    return new_bird.dict(), HTTPStatus.OK
