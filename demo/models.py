from django.db import models

from fdfsstorage.backends import FdfsStorage


# Create your models here.
class UploadFile(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    attachment = models.FileField(storage=FdfsStorage(), upload_to='test/upload/to/')
