# cloud/file_manager.py

from .storage import Client


class FileManager(object):
    """
    Interface to the S3 client to manage file uploads.
    """

    def __init__(self):
        """Constructor"""
        self.storage_client = Client()

    def upload_file(self, file_path: str, file_obj):
        """
        Attempt to upload a file to S3 using two methods, one for small and one for large files.

        :param file_path:
        :param file_obj:
        :return:
        """
        try:
            self.storage_client.upload_large_file(file_path, file_obj.temporary_file_path())
        except AttributeError:
            self.storage_client.upload_small_file(file_path, file_obj.read())

    def delete_file(self, file_path: str):
        """
        Attempt to delete a file saved in the bucket.

        :param file_path:
        :return:
        """
        self.storage_client.delete_object(file_path)
