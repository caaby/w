# -*- coding: utf-8 -*-

import os
from qiniu import Auth, put_file


def seven_cattle(**kwargs):
    # 构建鉴权对象
    q = Auth(kwargs.get("access_key"), kwargs.get("secret_key"))
    # 要上传文件的本地路径
    files = kwargs.get("files").split(",")
    for file_path in files:
        token = q.upload_token(bucket=kwargs.get("bucket_name"), key=file_path, expires=60 * 5)
        put_file(up_token=token, key=file_path, file_path=file_path)


if __name__ == '__main__':

    config = {
        'access_key': os.getenv("access_key"),  # 填你的access_key
        'secret_key': os.getenv("secret_key"),  # 填你的secret_key
        'bucket_name': os.getenv("bucket"),  # 填你的存储空间名称
        'files': os.getenv("files")
    }
    seven_cattle(**config)


