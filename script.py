# -*- coding: utf-8 -*-
import os
import oss2

yourAccessKeyId = os.environ.get('ACCESS_KEY_ID')
yourAccessKeySecret = os.environ.get('ACCESS_KEY_SECRET')
yourEndpoint = os.environ.get('ENDPOINT')
bucket_name = os.environ.get('BUCKET_NAME')

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth(yourAccessKeyId, yourAccessKeySecret)

# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称，例如examplebucket。
bucket = oss2.Bucket(auth, yourEndpoint, bucket_name)
# 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。
object_name = 'cloud.conf'
# 填写待上传的字符串。
# content = '{"age": 1}'
# 设置HTTP header，例如HTTP header的名称为Content-Type，值为'application/json; charset=utf-8'。
# bucket.put_object(object_name, content, headers={'Content-Type': 'application/json; charset=utf-8'})
bucket.put_object_from_file(key=object_name,
                            filename=object_name,
                            headers={'Content-Type': 'text/plain; charset=utf-8'}
                            )

