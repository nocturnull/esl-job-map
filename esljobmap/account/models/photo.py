# account/models/resume.py

import time

from django.db import models

from cloud.storage import build_storage_url
from cloud.settings import AWS_S3_PARENT_DIR


class Photo(models.Model):
    original_filename = models.CharField(max_length=512, default='')
    unique_filename = models.CharField(max_length=512, default='')
    created_at_date = models.DateTimeField('Date Uploaded', auto_now_add=True)

    @property
    def storage_path(self) -> str:
        return AWS_S3_PARENT_DIR + '/photo/{0}'.format(self.unique_filename)

    @property
    def cdn_url(self) -> str:
        return build_storage_url(self.storage_path)

    @classmethod
    def create_photo(cls, filename):
        unique_filename = str(int(time.time())) + '-' + filename
        new_resume = Photo.objects.create(original_filename=filename, unique_filename=unique_filename)
        return new_resume

    def __str__(self):
        return self.original_filename
