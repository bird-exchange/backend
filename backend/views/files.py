from http import HTTPStatus
from pathlib import Path

from flask import Blueprint, request
from werkzeug.utils import secure_filename

from backend.aws import s3
from backend.config import config
from botocore.exceptions import ClientError
from backend.errors import RequestNotContainError, AppError, NotAcceptableError
view = Blueprint('files', __name__)

ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])


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

    resp = s3.list_buckets()
    all_buckets_names = [bucket['Name'] for bucket in resp['Buckets']]

    for bucket_name in [config.aws.bucket_input_images, config.aws.bucket_output_images]:
        if bucket_name not in all_buckets_names:
            s3.create_bucket(Bucket=bucket_name)

    try:
        s3.upload_fileobj(file, config.aws.bucket_input_images, filename)
    except ClientError:
        raise AppError("Не удалось сохранить файл", HTTPStatus.NOT_IMPLEMENTED)

    return f'{filename} successfully saved', HTTPStatus.OK


@view.get('/<uid>')
def get_link_to_image():
    pass
