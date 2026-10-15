import datetime
import uuid
from enum import Enum

from model.common import CreateTimeBaseModel, UuidBaseModel, db
from service.oss import oss_client


class FileType(Enum):
    IMAGE = 'image'

class File(UuidBaseModel, CreateTimeBaseModel):
    type = db.Column(db.Enum(FileType), nullable=False, default=FileType.IMAGE)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    path = db.Column(db.String(100), nullable=False)
    references = db.Column(db.Integer, nullable=False, default=0)  # 被引用次数，如果为0则，没有地方用

    @classmethod
    def add_file(cls, content, ext,):
        """
        上传文件到oss，并添加记录
        :param content:
        :param ext: 文件后缀
        :param org_id:
        :return: (id, url)
        """
        path = f'prod/img/{str(uuid.uuid4())}.{ext}'
        obj = cls(path=path)
        db.session.add(obj)
        db.session.flush()
        oss_client.update_object(content, path)

        return obj
    
    @classmethod
    def reference(cls, _ids: list|str, delta=1):
        """
        引用次数增加或减少
        :param _ids: 图片id列表或字符串
        :param delta: 增加或减少的次数，默认增加1
        :return:
        """
        if not _ids:
            return
        if isinstance(_ids, str):
            _ids = [_ids]
        objs = cls.query.filter(cls.id.in_(_ids)).all()
        for obj in objs:
            obj.references += delta
        db.session.flush()
        # db.session.commit()
    
    @classmethod
    def deference(cls, _ids: list|str, delta=-1):
        """
        引用次数减少
        :param _ids: 图片id列表或字符串
        :param delta: 减少的次数，默认减少1
        :return:
        """
        cls.reference(_ids, delta)

    @classmethod
    def get_file_urls(cls, ids: list|str):
        if not ids:
            return ids

        if isinstance(ids, list):
            urls = []
            for item in cls.query.filter(cls.id.in_(ids)).all():
                urls.append(oss_client.sign_url(item.path))
            return urls
        else:
            obj = cls.query.filter(cls.id == ids).first()
            if not obj:
                return ids
            else:
                return oss_client.sign_url(obj.path)

    @classmethod
    def get_dict(cls, _id):
        obj = cls.query.get(_id)
        if not obj:
            return None
        return obj.to_dict()

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.get_file_urls(self.id)
        }






