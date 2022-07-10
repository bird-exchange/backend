from tests.factories import ImageFactory


def test_next_task_successed(client, session):
    image = ImageFactory.create()
    image.was_fitted = 0
    response = client.get('api/v1/task/')
    assert response.status_code == 200


def test_get_next_task_failed_notfounf(client, session):
    image = ImageFactory.create()
    image.was_fitted = 1
    response = client.get('api/v1/task/')
    assert response.status_code == 404
