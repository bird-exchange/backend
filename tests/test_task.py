from tests.factories import BirdFactory


def test_next_task_successed(client, session):
    bird = BirdFactory.create()
    bird.was_fitted = 0
    response = client.get('api/v1/task/')
    assert response.status_code == 200


def test_get_next_task_failed_notfounf(client, session):
    bird = BirdFactory.create()
    bird.was_fitted = 1
    response = client.get('api/v1/task/')
    assert response.status_code == 404
