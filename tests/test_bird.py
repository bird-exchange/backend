import random

from tests.factories import BirdFactory


def test_add_bird_successed(client, session):
    bird_data = {
        "name": "test_bird3",
        "type": 1,
        "was_fitted": 0
    }
    response = client.post('/api/v1/bird/', json=bird_data)
    assert response.status_code == 201


def test_add_bird_failed_conflict(client, session):
    bird = BirdFactory.create()
    bird_data = {
        "name": bird.name,
        "type": 1,
        "was_fitted": 0
    }
    response = client.post('/api/v1/bird/', json=bird_data)
    assert response.status_code == 409


def test_add_bird_failed_badrequest(client, session):
    bird_data = {
        "bird_name": "test_bird",
        "type": 1,
        "was_fitted": 0
    }
    response = client.post('/api/v1/bird/', json=bird_data)
    assert response.status_code == 400


def test_get_all_successed(client, session):
    number = random.randint(0, 100)
    for _ in range(number):
        BirdFactory.create()

    response = client.get('/api/v1/bird/')
    assert response.status_code == 200

    recieved_birds = response.json
    assert len(recieved_birds) == number


def test_get_by_id_successed(client, session):
    bird = BirdFactory.create()
    response = client.get(f'api/v1/bird/{bird.uid}')
    assert response.status_code == 200

    recieved_bird = response.json
    assert recieved_bird['name'] == bird.name


def test_get_by_id_failed_notfound(client, session):
    bird = BirdFactory.create()
    response = client.get(f'api/v1/bird/{bird.uid + 1}')
    assert response.status_code == 404


def test_delete_all(client, session):
    for _ in range(10):
        BirdFactory.create()
    response = client.delete('api/v1/bird/')
    assert response.status_code == 204


def test_delete_by_id_successed(client, session):
    bird = BirdFactory.create()
    response = client.delete(f'api/v1/bird/{bird.uid}')
    assert response.status_code == 204


def test_delete_by_id_failed_notfound(client, session):
    bird = BirdFactory.create()
    response = client.delete(f'api/v1/bird/{bird.uid + 1}')
    assert response.status_code == 404


def test_update_by_id_bird_successed(client, session):
    bird = BirdFactory.create()
    new_bird = {
        "name": "test_name",
        "type": 1
    }
    response = client.put(f'api/v1/bird/{bird.uid}', json=new_bird)
    assert response.status_code == 200


def test_update_by_id_bird_failed_notfound(client, session):
    bird = BirdFactory.create()
    new_bird = {
        "name": "test_name",
        "type": 1
    }
    response = client.put(f'api/v1/bird/{bird.uid + 1}', json=new_bird)
    assert response.status_code == 404


def test_update_by_id_bird_failed_badrequest(client, session):
    bird = BirdFactory.create()
    new_bird = {
        "bird_name": "test_name",
        "type": 1,
    }
    response = client.put(f'api/v1/bird/{bird.uid}', json=new_bird)
    assert response.status_code == 400
