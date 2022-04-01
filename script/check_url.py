# -*- coding: utf-8 -*-

import os
from qiniu import Auth, BucketManager


def seven_cattle(**kwargs):
    # 构建鉴权对象
    q = Auth(kwargs.get("access_key"), kwargs.get("secret_key"))
    BucketManager(auth=q).fetch(url=kwargs.get("bucket_name"), bucket=kwargs.get("bucket_name"), key="list")


if __name__ == '__main__':

    config = {
        'access_key': os.getenv("access_key"),  # 填你的access_key
        'secret_key': os.getenv("secret_key"),  # 填你的secret_key
        'bucket_name': os.getenv("bucket"),  # 填你的存储空间名称
    }
    seven_cattle(**config)


