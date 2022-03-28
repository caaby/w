from qiniu import Auth, put_file, etag


def seven_cattle(**kwargs):

    # 构建鉴权对象
    q = Auth(kwargs.get("access_key"), kwargs.get("secret_key"))
    # 上传后保存的文件名
    key = 'my-python-logo.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(kwargs.get("bucket_name"), key, 60*5)
    # 要上传文件的本地路径
    files = kwargs.get("files").split(",")
    for file_path in files:
        token = q.upload_token(bucket=kwargs.get("bucket_name"), key=file_path, expires=60 * 5)
        ret, info = put_file(up_token=token, key=file_path, file_path=file_path, version='v2')
        assert ret['key'] == key
        assert ret['hash'] == etag(file_path)


if __name__ == '__main__':
    import os

    config = {
        'access_key': os.getenv("access_key"),  # 填你的access_key
        'secret_key': os.getenv("secret_key"),  # 填你的secret_key
        'bucket_name': os.getenv("bucket"),  # 填你的存储空间名称
        'files': os.getenv("files")
    }
    print(config)
    seven_cattle(**config)


