import os


def test_config_using_test_db(app):
    assert app.config['DATABASE_URL'] == os.environ['TEST_DB_URL']
