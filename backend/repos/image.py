from http import HTTPStatus

from botocore.exceptions import ClientError

from backend.aws import s3_client, s3_resource
from backend.errors import AppError


class ImageRepo():
    name = "image"

    def create_buckets(self, buckets: list[str]) -> None:
        resp = s3_client.list_buckets()
        existed_buckets = [bucket['Name'] for bucket in resp['Buckets']]
        for bucket in buckets:
            if bucket not in existed_buckets:
                s3_client.create_bucket(Bucket=bucket)

    def upload_file_to_bucket(self, file, bucket_input: str, filename: str) -> None:
        try:
            s3_client.upload_fileobj(file, bucket_input, filename)
        except ClientError:
            raise AppError(f"Failed to save {self.name}", HTTPStatus.NOT_IMPLEMENTED)

    def delete_image_by_name(self, bucket: str, filename: str):
        try:
            s3_client.delete_object(Bucket=bucket, Key=filename)
        except ClientError:
            pass

    def delete_all(self, bucket_name: str):
        try:
            bucket = s3_resource.Bucket(bucket_name)
            bucket.objects.all().delete()
        except ClientError:
            pass
