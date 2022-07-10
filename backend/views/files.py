from http import HTTPStatus
from pathlib import Path

from botocore.exceptions import ClientError
from flask import Blueprint, request
from werkzeug.utils import secure_filename

from backend.aws import s3
from backend.config import config
from backend.errors import AppError, NotAcceptableError, RequestNotContainError
from backend.repos.images import ImageRepo
from backend import schemas

view = Blueprint('files', __name__)
image_repo = ImageRepo()

ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])


def create_buckets(buckets: list[str]) -> None:
    resp = s3.list_buckets()
    existed_buckets = [bucket['Name'] for bucket in resp['Buckets']]
    for bucket in buckets:
        if bucket not in existed_buckets:
            s3.create_bucket(Bucket=bucket)


def upload_image_to_bucket(file, bucket_input: str, filename: str) -> None:
    try:
        s3.upload_fileobj(file, bucket_input, filename)
    except ClientError:
        raise AppError("Failed to save file", HTTPStatus.NOT_IMPLEMENTED)


def get_image_url(bucket: str, filename: str) -> str:
    try:
        return s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': filename},
            ExpiresIn=3600
        )
    except ClientError:
        raise AppError("Failed to access file", HTTPStatus.NOT_FOUND)


@view.post('/')
def upload_image():
    if not ('file' in request.files):
        raise RequestNotContainError('file')
    file = request.files['file']
    if not file.filename:
        raise RequestNotContainError('file')
    filename = secure_filename(file.filename)
    if not (Path(filename).suffix in ALLOWED_EXTENSIONS):
        raise NotAcceptableError('file format')

    bucket_input = config.aws.bucket_input_images
    bucket_output = config.aws.bucket_output_images

    create_buckets([bucket_input, bucket_output])

    upload_image_to_bucket(file, bucket_input, filename)

    image_data = {
        "uid": -1,
        "name": filename,
        "type": 1,
        "was_fitted": 0
    }
    image_data = schemas.Image(**image_data)
    image_repo.add_image(**image_data.dict())

    return f'{filename} successfully saved', HTTPStatus.CREATED


@view.get('/<uid>')
def get_link_to_image_by_id():
    pass
