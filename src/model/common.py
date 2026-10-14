import datetime
import uuid
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import pymysql
from sqlalchemy.orm import declared_attr

pymysql.install_as_MySQLdb()

metadata = MetaData(naming_convention={
    "default_collation": "utf8mb4_general_ci"
})

db = SQLAlchemy(metadata=metadata)


class ToDictBaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, cols=None):
        columns = cols if cols else [col.name for col in self.__table__.columns]
        result = {}
        for col in columns:
            v = getattr(self, col)
            if isinstance(v, datetime.datetime):
                v = v.strftime('%Y-%m-%d')
            elif isinstance(v, Enum):
                v = v.value
            result[col] = v
        return result

class CreateTimeBaseModel(db.Model):
    __abstract__ = True
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class OrgBaseModel(db.Model):
    __abstract__ = True
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    # organization = db.relationship("Organization", foreign_keys=[org_id], lazy=True)

    @declared_attr
    def organization(self):
        return db.relationship("Organization", foreign_keys=[self.org_id], lazy=True)

class UuidBaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class CommonModel(UuidBaseModel, CreateTimeBaseModel, OrgBaseModel, ToDictBaseModel):
    __abstract__ = True

