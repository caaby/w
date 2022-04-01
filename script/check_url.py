# -*- coding: utf-8 -*-

import os
from qiniu import Auth, BucketManager


def seven_cattle(**kwargs):
    # 构建鉴权对象
    q = Auth(kwargs.get("access_key"), kwargs.get("secret_key"))
    bucket = BucketManager(q)
    key = "free.list"
    ret, info = bucket.fetch(url=kwargs.get("url"), bucket=kwargs.get("bucket_name"), key=key)
    print(info)
    assert ret['key'] == key
    # 将一个文件的元信息修改为jpg
    ret, info = bucket.change_mime(kwargs.get("bucket_name"), key, 'text/plain; charset=utf-8')
    print(info)

if __name__ == '__main__':

    config = {
        'access_key': os.getenv("access_key"),  # 填你的access_key
        'secret_key': os.getenv("secret_key"),  # 填你的secret_key
        'bucket_name': os.getenv("bucket"),  # 填你的存储空间名称
        'url': os.getenv("url")
    }
    seven_cattle(**config)


