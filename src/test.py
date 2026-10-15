import datetime
import os
from unittest import TestCase

from werkzeug.security import generate_password_hash

import app
from model.common import db
from model.file import File
from service.oss import oss_client



class TestOss(TestCase):
    def setUp(self):
        self.app = app.app  # 创建应用实例
        self.app_context = self.app.app_context()
        self.app_context.push()  # 推入应用上下文
        self.path = 'test/img.png'

    # def tearDown(self):
    #     self.app_context.pop()  # 弹出应用上下文

    def test_oss(self):

        # with open('./img.png', 'rb') as f:
        #     oss_client.update_object(f.read(), path)
        print(oss_client.sign_url(self.path))

    def test_upload_image(self):
        with open('./img.png', 'rb') as f:
            File.add_prod_img(content=f.read(), ext='png', org_id=1)
            db.session.commit()
            

class TestWanxiang(TestCase):
    
    def setUp(self):
        self.app = app.app  # 创建应用实例
        self.app_context = self.app.app_context()
        self.app_context.push()  # 推入应用上下文

    def test_update_image(self):
        """局部更新"""
        pass

    def test_re_image(self):
        """基于已有图重新构图"""
        from service.wanxiang import wanxiang_client
        base_url = "https://order-management-20251103.oss-cn-wuhan-lr.aliyuncs.com/test/img.png?Expires=1792055453&OSSAccessKeyId=TMP.3Kysg5ypSWaYr5pGciZCTa9D1CoPVwJm1iZ6BjF4tyqJgxbm28WbJ2EavajumufEk3pzdEXPtHvXzNyR6aiNZF6Hj7ojtX&Signature=FXYWGSsuVz4S2sWp%2ByUiblPtEcA%3D"
        wanxiang_client.image_synthesis(
            prompt="只保留右侧的柱状图部分，其他部分剪切掉", 
            base_image_url=base_url,
        )


# if __name__ == "__main__":
    # test_pdf()
    # test_excel()
    # test_pdf_labels()
#     test_oss()
    # test_pwd()
    # python -m unittest test.TestPermission.test_auto_fill_permissions
    # pass


