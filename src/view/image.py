import imghdr

import werkzeug
from flask import redirect
from flask_restful import reqparse

from model.common import db
from model.file import File
from service.oss import oss_client
from view.common import PathViewV1


class Image(PathViewV1):
    """处理产品相关的图片上传"""
    _path = "/api/v1/img"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    REQUIRED_PERMISSIONS = []

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        uploaded_file = args['file']

        # 验证文件类型
        filename = uploaded_file.filename
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext not in self.ALLOWED_EXTENSIONS:
            return {"status": "error", 'message': f"只支持{self.ALLOWED_EXTENSIONS} 格式的图片"}

        # 验证图片内容
        if not self.is_valid_image(uploaded_file):
            return {"status": "error", 'message': '无法识别当前图片'}
        # 保存文件
        uploaded_file.seek(0)  # 重置到文件开头
        obj = File.add_prod_img(content=uploaded_file.read(), ext=ext, org_id=self.current_user.org_id)
        db.session.commit()
        return {'status': 'status', "id": obj.id, "url": oss_client.sign_url(obj.path), "name": obj.path.split("/")[-1]}


    @classmethod
    def is_valid_image(cls, file_storage):
        # 重置文件指针
        file_storage.seek(0)
        # 检查图片头部信息
        header = file_storage.read(512)
        file_storage.seek(0)
        format = imghdr.what(None, header)
        return format is not None

class ImagePreview(PathViewV1):
    """访问图片"""
    _path = "/api/v1/img/<img_id>"
    REQUIRED_PERMISSIONS = [PermissionBase.LOGIN]

    def post(self, img_id):
        img = File.query.filter(File.id==img_id, File.org_id==self.current_user.org_id).first()
        if not img:
            return {"status": "error", 'message': '图片不存在'}

        return redirect(oss_client.sign_url(img.path))

    def delete(self, img_id):
        img = File.query.filter(File.id == img_id, File.org_id == self.current_user.org_id).first()
        if not img:
            return {'status': 'success'}
        oss_client.delete_object(img.path)
        db.session.delete(img)
        db.session.commit()
        return {'status': 'success'}