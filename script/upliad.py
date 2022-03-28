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
        :param domain:
        :param bucket_name:
        """
        need_key = ('access_key', 'secret_key', 'domain', 'bucket_name')
        for key in need_key:
            val = kwargs.get(key, None)
            if not val:
                raise ValueError('{} is necessary.'.format(key))
            setattr(self, key, val)

        self._q = Auth(self.access_key, self.secret_key)

    def upload(self, source_file_path, save_file_name):
        """
        :param source_file_path: 源文件路径
        :param save_file_name: 保存至七牛云的文件名
        :return:
        """
        token = self._q.upload_token(self.bucket_name, save_file_name)
        ret, info = put_data(token, source_file_path, save_file_name)
        if info.status_code == 200:
            return '/' . join([self.domain, save_file_name])
        return None


if __name__ == '__main__':
    import os

    config = {
        'access_key': os.getenv("access_key"),  # 填你的access_key
        'secret_key': os.getenv("secret_key"),  # 填你的secret_key
        'bucket_name': os.getenv("bucket"),  # 填你的存储空间名称
        'domain': 'cdn.caaby.com'  # 填你的空间域名
    }

    print(config)
    seven_cattle = SevenCattle(**config)
    url = seven_cattle.upload('main.py', 'main.py')
    print(url)
