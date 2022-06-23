from flask import Blueprint


view = Blueprint('task', __name__)


@view.get('/')
def get_next_task():
    pass
