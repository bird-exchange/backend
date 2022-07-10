from http import HTTPStatus

from flask import Blueprint

from backend import schemas
from backend.repos.image import Image

view = Blueprint('task', __name__)
image_repo = Image()


@view.get('/')
def get_next_task():
    entity = image_repo.get_not_recognized()
    image = schemas.Image.from_orm(entity)
    return image.dict(), HTTPStatus.OK
