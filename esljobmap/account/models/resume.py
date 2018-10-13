# account/models/resume.py

import time

from django.db import models

from cloud.storage import build_storage_url


class Resume(models.Model):
    filename = models.CharField(max_length=512, default='')
    created_at_date = models.DateTimeField('Date Uploaded', auto_now_add=True)

    @property
    def storage_path(self) -> str:
        return 'resume/{0}'.format(self.filename)

    @property
    def cdn_url(self) -> str:
        return build_storage_url(self.storage_path)

    @classmethod
    def create_resume(cls, filename):
        unique_filename = str(int(time.time())) + '-' + filename
        new_resume = Resume.objects.create(filename=unique_filename)
        return new_resume

    def __str__(self):
        return self.filename
