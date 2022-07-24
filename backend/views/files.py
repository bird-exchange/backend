from http import HTTPStatus
from pathlib import Path

from flask import Blueprint, request
from werkzeug.utils import secure_filename

from backend import schemas
from backend.config import config
from backend.errors import NotAcceptableError, RequestNotContainError
from backend.repos.files import FilesRepo
from backend.repos.image import ImageRepo

view = Blueprint('files', __name__)
image_repo = ImageRepo()
files_repo = FilesRepo()

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

    files_repo.create_buckets([bucket_input, bucket_output])

    files_repo.upload_file_to_bucket(file, bucket_input, filename)

    image_data = {
        "uid": -1,
        "name": filename,
        "type": 1,
        "was_fitted": 0
    }
    image_data = schemas.Image(**image_data)
    image_repo.add_image(**image_data.dict())

    return f'{filename} successfully saved', HTTPStatus.CREATED


@view.get('/origin/<uid>')
def get_presigned_url_origin_file_by_id(uid: int):
    entity = image_repo.get_by_id(uid)
    image = schemas.Image.from_orm(entity)
    return files_repo.get_file_url(bucket_input, image.name)


@view.get('/result/<uid>')
def get_presigned_url_result_file_by_id(uid: int):
    entity = image_repo.get_by_id(uid)
    image = schemas.Image.from_orm(entity)
    return files_repo.get_file_url(bucket_output, image.name)


@view.post('/result/')
def upload_result_file():
    if not ('file' in request.files):
        raise RequestNotContainError('file')
    file = request.files['file']
    if not file.filename:
        raise RequestNotContainError('file')
    filename = secure_filename(file.filename)
    if not (Path(filename).suffix in ALLOWED_EXTENSIONS):
        raise NotAcceptableError('file format')

    files_repo.create_buckets([bucket_input, bucket_output])

    files_repo.upload_file_to_bucket(file, bucket_output, filename)

    return f'{filename} successfully saved', HTTPStatus.CREATED
