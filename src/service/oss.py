import oss2

from setting import settings


class AliOSS2:
    def __init__(self):
        # 配置认证信息
        self.auth = oss2.Auth(settings.oss_access_id, settings.oss_access_secret)
        # 外网：oss-cn-wuhan-lr.aliyuncs.com, 内网： oss-cn-wuhan-lr-internal.aliyuncs.com
        self.bucket = oss2.Bucket(self.auth, 'http://oss-cn-wuhan-lr.aliyuncs.com', 'order-management-20251103')

    def upload_file(self, file_path, object_name):
        # 上传本地文件
        self.bucket.put_object_from_file(object_name, file_path)

    def update_object(self, content, object_name):
        # 上传字符串内容
        self.bucket.put_object(object_name, content)

    def download_file(self, file_path, object_name):
        # 下载到本地文件
        self.bucket.get_object_to_file(object_name, file_path)

    def get_object(self, object_name):
        # 获取对象内容
        result = self.bucket.get_object(object_name)
        content = result.read()
        return content

    def delete_object(self, object_name):
        # 删除对象
        self.bucket.delete_object(object_name)

    def list_objects(self):
        # 列出Bucket中的所有文件
        return [obj.key for obj in oss2.ObjectIterator(self.bucket)]

    def sign_url(self, object_name, expires_in=600):
        # 生成签名 URL
        url = self.bucket.sign_url('GET', object_name, expires_in)
        return url


    # # 处理异常
    # try:
    #     self.bucket.put_object('<object-key>', 'Hello OSS')
    # except oss2.exceptions.OssError as e:
    #     print(f"OSS Error: {e}")

oss_client = AliOSS2()