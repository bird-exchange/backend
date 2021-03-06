import boto3

from backend.config import config

session = boto3.session.Session()

s3_client = session.client(
    service_name='s3',
    endpoint_url='http://127.0.0.1:9000',
    aws_access_key_id=config.aws.key_id,
    aws_secret_access_key=config.aws.key,
)

s3_resource = boto3.resource(
    service_name='s3',
    endpoint_url='http://127.0.0.1:9000',
    aws_access_key_id=config.aws.key_id,
    aws_secret_access_key=config.aws.key,
)
