# cloud/storage.py

import boto3

from .settings import *


class Client(object):
    """
    AWS S3 client connection.

    Used to interface with a bucket.
    https://boto3.readthedocs.io/en/latest/reference/services/s3.html
    """

    def __init__(self):
        """Constructor"""
        self.bucket = boto3.resource('s3').Bucket(AWS_S3_BUCKET)

    def upload_small_file(self, skey, fobject):
        """
        Wrapper function to upload a small file to the S3 bucket.

        Refer to the S3 bucket.put_object file function docs.
        https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Bucket.put_object
        :param skey:
        :param fobject:
        :return:
        """
        self.bucket.put_object(Key=skey, Body=fobject, ACL='public-read')

    def upload_large_file(self, skey, fpath):
        """
        Wrapper function to upload a large file to the S3 bucket.

        Refer to the S3 bucket.upload file function docs
        https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Bucket.upload_file
        :param skey:
        :param fpath:
        :return:
        """

        self.bucket.upload_file(
            Filename=fpath,
            Key=skey,
            ExtraArgs={
                'ACL': 'public-read'
            })


def build_storage_url(uri: str) -> str:
    return AWS_S3_BASE_LINK.format(
        os.environ.get('AWS_DEFAULT_REGION'),
        AWS_S3_BUCKET,
        uri
    )
