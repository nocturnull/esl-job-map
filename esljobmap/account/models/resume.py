# account/models/resume.py

import time
import os

from django.db import models

from cloud.storage import build_cdn_url, build_s3_url
from cloud.settings import AWS_S3_PARENT_DIR


class Resume(models.Model):
    original_filename = models.CharField(max_length=512, default='')
    unique_filename = models.CharField(max_length=512, default='')
    created_at_date = models.DateTimeField('Date Uploaded', auto_now_add=True)

    @property
    def storage_path(self) -> str:
        return AWS_S3_PARENT_DIR + '/resume/{0}'.format(self.unique_filename)

    @property
    def cdn_url(self) -> str:
        if os.environ.get('ESLJOBMAP_LOAD_REMOTE', None) is not None:
            return build_cdn_url('resume/{0}'.format(self.unique_filename))
        return build_s3_url(self.storage_path)

    @classmethod
    def create_resume(cls, filename):
        unique_filename = str(int(time.time())) + '-' + filename
        new_resume = Resume.objects.create(original_filename=filename, unique_filename=unique_filename)
        return new_resume

    def __str__(self):
        return self.original_filename
