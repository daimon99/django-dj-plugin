# coding: utf-8
import os
from io import BytesIO

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_bytes, force_text


@deconstructible
class FdfsStorage(Storage):
    """
    Fdfs Storage Service
    """
    location = ""

    def __init__(self, option=None):
        if not option:
            option = getattr(settings, 'FDFS_OPTIONS', {})
        self.FDFS_PATH = '/usr/local/bin/fdfs_upload_file'
        self.CONF_PATH = '/etc/fdfs/client.conf'

    def _open(self, name, mode='rb'):
        return FdfsFile(name, self, mode)

    def _save(self, name, content):
        print(name, content)

        raise NotImplementedError()

    def _read(self, current_pos, num_bytes):
        raise NotImplementedError()

    def path(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

    def exists(self, name):
        return False

    def listdir(self):
        raise NotImplementedError()

    def size(self, name):
        raise NotImplementedError()

    def url(self):
        raise NotImplementedError()


class FdfsFile(File):
    def init(self, name, storage, mode):
        self.file = BytesIO()
        self._mode = mode
        self._name = name
        self._storage = storage
        self._is_dirty = False
        self._is_read = False

    @property
    def size(self):
        if self._is_dirty or self._is_read:
            # Get the size of a file like object
            # Check http://stackoverflow.com/a/19079887
            old_file_position = self.file.tell()
            self.file.seek(0, os.SEEK_END)
            self._size = self.file.tell()
            self.file.seek(old_file_position, os.SEEK_SET)
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        # todo 大文件读取会有问题。以后优化。应该支持chunk 读的方式。现在是一口气把所有内容都读出来了。
        if not self._is_read:
            current_pos = 0
            content = self._storage._read(self._name, current_pos, num_bytes)
            self.file = BytesIO(content)
            self._is_read = True

        if num_bytes is None:
            data = self.file.read()
        else:
            data = self.file.read(num_bytes)

        if 'b' in self._mode:
            return data
        else:
            return force_text(data)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file.write(force_bytes(content))
        self._is_dirty = True
        self._is_read = True

    def close(self):
        if self._is_dirty:
            self.file.seek(0)
            self._storage._save(self._name, self.file)
        self.file.close()


class FdfsDriver(object):
    @staticmethod
    def upload_file():
        pass
