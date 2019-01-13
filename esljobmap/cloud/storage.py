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
        self.bucket.put_object(Key=skey, Body=fobject, ContentDisposition='inline',
                               ContentType=self._detect_content_type(skey), ACL='public-read')

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
                'ContentDisposition': 'inline',
                'ContentType': self._detect_content_type(skey),
                'ACL': 'public-read'
            })

    def delete_object(self, skey):
        """
        Wrapper function to the delete_objects method for the S3 bucket.

        :param skey:
        :return:
        """
        self.bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': skey
                    }
                ],
                'Quiet': True
            }
        )

    @classmethod
    def _detect_content_type(cls, path):
        if 'pdf' in path:
            return 'application/pdf'
        elif 'gif' in path:
            return 'image/gif'
        elif 'jpg' in path or 'jpeg' in path:
            return 'image/jpeg'
        elif 'png' in path:
            return 'image/png'
        return 'application/msword'


def build_storage_url(uri: str) -> str:
    return AWS_CDN_BASE_LINK + uri
