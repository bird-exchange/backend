import os

from pydantic import BaseModel


class Server(BaseModel):
    port: str
    host: str


class DataBase(BaseModel):
    url: str


class AwsConfig(BaseModel):
    key_id: str
    key: str
    bucket_input_images: str
    bucket_output_images: str


class AppConfig(BaseModel):
    server: Server
    db: DataBase
    aws: AwsConfig


def load_from_env() -> AppConfig:
    app_port = os.environ['APP_PORT']
    app_host = os.environ['APP_HOST']
    db_url = os.environ['DB_URL']
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_bucket_input_images = os.environ['AWS_BUCKET_NAME_INPUT_IMAGES']
    aws_bucket_output_images = os.environ['AWS_BUCKET_NAME_OUTPUT_IMAGES']
    return AppConfig(
        server=Server(port=app_port, host=app_host),
        db=DataBase(url=db_url),
        aws=AwsConfig(
            key_id=aws_access_key_id,
            key=aws_secret_access_key,
            bucket_input_images=aws_bucket_input_images,
            bucket_output_images=aws_bucket_output_images,
        )
    )


def get_config(test_config=False) -> AppConfig:
    if not test_config:
        return load_from_env()
    test_config = load_from_env()
    db_url = os.environ['TEST_DB_URL']
    test_config.db.url = db_url
    return test_config
