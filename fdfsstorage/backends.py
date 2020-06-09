# coding: utf-8

import os

from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client, get_tracker_conf


class FdfsStorage(Storage):
    def __init__(self, base_url='http://', client_conf=None):
        """
        初始化
        :param base_url: 用于构造图片完整路径使用，图片服务器的域名
        :param client_conf: FastDFS客户端配置文件的路径
        """
        if base_url is None:
            # base_url = settings.FDFS_URL
            base_url = 'http://localhost'
        self.base_url = base_url
        if client_conf is None:
            # client_conf = settings.FDFS_CLIENT_CONF
            client_conf = '/etc/fdfs/client.conf'
        self.client_conf = client_conf

    def _open(self, name, mode='rb'):
        """
        用不到打开文件，所以省略
        """
        pass

    def _save(self, name, content):
        """
        在FastDFS中保存文件
        :param name: 传入的文件名
        :param content: 文件内容
        :return: 保存到数据库中的FastDFS的文件名
        """
        # {
        # 'Local file name': '/home/python/1.jpg',
        # 'Storage IP': '192.168.189.133',
        # 'Remote file_id': 'group1/M00/00/00/wKi9hVz-Pm-Ab2WUAAOTipWhnKM344.jpg',
        #  'Group name': 'group1',
        # 'Status': 'Upload successed.',
        # 'Uploaded size': '228.00KB'
        # }
        client = Fdfs_client(get_tracker_conf(self.client_conf))  # 实例化一个Fdfs_client对象
        dir_name, file_name = os.path.split(name)
        file_ext_name = file_name.split('.')[-1]
        ret = client.upload_by_buffer(content.read(), file_ext_name, {
            'dir': dir_name,
            'name': file_name,
            'namespace': 'default'
        })  # 根据内容上传
        if ret.get("Status") != "Upload successed.":
            raise Exception("upload file failed")
        file_name = ret.get("Remote file_id")
        return file_name.decode()

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        return self.base_url + name

    def exists(self, name):
        """
        判断文件是否存在，FastDFS可以自行解决文件的重名问题
        所以此处返回False，告诉Django上传的都是新文件
        :param name:  文件名
        :return: False
        """
        return False
