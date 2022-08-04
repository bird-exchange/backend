from http import HTTPStatus

from flask import Blueprint

from backend import schemas
from backend.repos.bird import BirdRepo

view = Blueprint('task', __name__)
bird_repo = BirdRepo()


@view.get('/')
def get_next_task():
    entity = bird_repo.get_not_recognized()
    bird = schemas.Bird.from_orm(entity)
    return bird.dict(), HTTPStatus.OK
