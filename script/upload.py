from qiniu import Auth, put_data


class SevenCattle:
    """
    单例模式七牛云文件上传
    """
    __instance = None

    def __new__(cls, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, **kwargs):
        """
        :param access_key:
        :param secret_key:
        :param bucket_name:
        """

        self.access_key = kwargs.get("access_key")
        self.secret_key = kwargs.get("secret_key")
        self.bucket_name = kwargs.get("bucket_name")
        self._q = Auth(self.access_key, self.secret_key)

    def upload(self, source_file_path, save_file_name):
        """
        :param source_file_path: 源文件路径
        :param save_file_name: 保存至七牛云的文件名
        :return:
        """
        token = self._q.upload_token(self.bucket_name, save_file_name)
        put_data(token, source_file_path, save_file_name)


if __name__ == '__main__':
    import os

    config = {
        'access_key': os.getenv("access_key"),  # 填你的access_key
        'secret_key': os.getenv("secret_key"),  # 填你的secret_key
        'bucket_name': os.getenv("bucket"),  # 填你的存储空间名称
    }

    seven_cattle = SevenCattle(**config)
    seven_cattle.upload('../c.conf', 'surge')

