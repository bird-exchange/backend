from http import HTTPStatus
from pathlib import Path

from flask import Blueprint, request
from werkzeug.utils import secure_filename

from backend import schemas
from backend.config import config
from backend.errors import NotAcceptableError, RequestNotContainError
from backend.repos.image import ImageRepo
from backend.repos.bird import BirdRepo

view = Blueprint('image', __name__)
bird_repo = BirdRepo()
image_repo = ImageRepo()

ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])

bucket_input = config.aws.bucket_input_images
bucket_output = config.aws.bucket_output_images


@view.post('/')
def upload_file():
    if not ('file' in request.files):
        raise RequestNotContainError('file')
    file = request.files['file']
    if not file.filename:
        raise RequestNotContainError('file')
    filename = secure_filename(file.filename)
    if not (Path(filename).suffix in ALLOWED_EXTENSIONS):
        raise NotAcceptableError('file format')
    if not request.args['kind']:
        raise RequestNotContainError('kind')

    kind = request.args['kind']
    if kind == 'sparrow':
        type = 2
    elif kind == 'tit':
        type = 1

    image_repo.create_buckets([bucket_input, bucket_output])

    image_repo.upload_file_to_bucket(file, bucket_input, filename)

    bird_data = {
        "uid": -1,
        "name": filename,
        "type": type,
        "was_fitted": 0
    }
    bird_data = schemas.Bird(**bird_data)
    bird_repo.add_bird(**bird_data.dict())

    return f'{filename} successfully saved', HTTPStatus.CREATED


@view.post('/result/')
def upload_result_image():
    if not ('file' in request.files):
        raise RequestNotContainError('file')
    file = request.files['file']
    if not file.filename:
        raise RequestNotContainError('file')
    filename = secure_filename(file.filename)
    if not (Path(filename).suffix in ALLOWED_EXTENSIONS):
        raise NotAcceptableError('file format')

    image_repo.create_buckets([bucket_input, bucket_output])

    image_repo.upload_file_to_bucket(file, bucket_output, filename)

    return f'{filename} successfully saved', HTTPStatus.CREATED
