import random

from tests.factories import ImageFactory


def test_add_image_successed(client, session):
    image_data = {
        "name": "test_image3",
        "type": 1,
        "was_fitted": 0
    }
    response = client.post('/api/v1/image/', json=image_data)
    assert response.status_code == 201


def test_add_image_failed_conflict(client, session):
    image = ImageFactory.create()
    image_data = {
        "name": image.name,
        "type": 1,
        "was_fitted": 0
    }
    response = client.post('/api/v1/image/', json=image_data)
    assert response.status_code == 409


def test_add_image_failed_badrequest(client, session):
    image_data = {
        "image_name": "test_image",
        "type": 1,
        "was_fitted": 0
    }
    response = client.post('/api/v1/image/', json=image_data)
    assert response.status_code == 400


def test_get_all_successed(client, session):
    number = random.randint(0, 100)
    for _ in range(number):
        ImageFactory.create()

    response = client.get('/api/v1/image/')
    assert response.status_code == 200

    recieved_images = response.json
    assert len(recieved_images) == number


def test_get_by_id_successed(client, session):
    image = ImageFactory.create()
    response = client.get(f'api/v1/image/{image.uid}')
    assert response.status_code == 200

    recieved_image = response.json
    assert recieved_image['name'] == image.name


def test_get_by_id_failed_notfound(client, session):
    image = ImageFactory.create()
    response = client.get(f'api/v1/image/{image.uid + 1}')
    assert response.status_code == 404


def test_delete_all(client, session):
    for _ in range(10):
        ImageFactory.create()
    response = client.delete('api/v1/image/')
    assert response.status_code == 204


def test_delete_by_id_successed(client, session):
    image = ImageFactory.create()
    response = client.delete(f'api/v1/image/{image.uid}')
    assert response.status_code == 204


def test_delete_by_id_failed_notfound(client, session):
    image = ImageFactory.create()
    response = client.delete(f'api/v1/image/{image.uid + 1}')
    assert response.status_code == 404


def test_update_by_id_image_successed(client, session):
    image = ImageFactory.create()
    new_image = {
        "name": "test_name",
        "type": 1
    }
    response = client.put(f'api/v1/image/{image.uid}', json=new_image)
    assert response.status_code == 200


def test_update_by_id_image_failed_notfound(client, session):
    image = ImageFactory.create()
    new_image = {
        "name": "test_name",
        "type": 1
    }
    response = client.put(f'api/v1/image/{image.uid + 1}', json=new_image)
    assert response.status_code == 404


def test_update_by_id_image_failed_badrequest(client, session):
    image = ImageFactory.create()
    new_image = {
        "image_name": "test_name",
        "type": 1,
    }
    response = client.put(f'api/v1/image/{image.uid}', json=new_image)
    assert response.status_code == 400
