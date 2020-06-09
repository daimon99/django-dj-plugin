# coding: utf-8

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class FdfsStorage(Storage):
    """
    Fdfs Storage Service
    """
    location = ""

    def __init__(self, option=None):
        if not option:
            option = settings.FDFS_OPTIONS
        self.FDFS_PATH = '/usr/local/bin/fdfs_upload_file'
        self.CONF_PATH = '/etc/fdfs/client.conf'

    def _open(self, name, mode='rb'):
        raise NotImplementedError()

    def _save(self):
        raise NotImplementedError()

    def path(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def exists(self):
        raise NotImplementedError()

    def listdir(self):
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    def url(self):
        raise NotImplementedError()


