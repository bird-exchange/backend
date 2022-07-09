from tests.factories import ImageFactory


def test_add_image_successed(client, session):
    image_data = {
        "name": "test_image3",
        "type": 1,
        "path_original": "test",
        "path_result": "test",
        "was_fitted": 0
    }
    response = client.post('/api/v1/image/', json=image_data)
    assert response.status_code == 201


def test_add_image_failed_conflict(client, session):
    image = ImageFactory.create()
    image_data = {
        "name": image.name,
        "type": 1,
        "path_original": "test",
        "path_result": "test",
        "was_fitted": 0
    }
    response = client.post('/api/v1/image/', json=image_data)
    assert response.status_code == 409


def test_get_all_successed(client, session):
    ImageFactory.create()

    response = client.get('/api/v1/image/')
    assert response.status_code == 200


def test_add_image_failed_badrequest(client, session):
    image_data = {
        "image_name": "test_image",
        "type": 1,
        "path_original": "test",
        "path_result": "test",
        "was_fitted": 0
    }
    response = client.post('/api/v1/image/', json=image_data)
    assert response.status_code == 400
