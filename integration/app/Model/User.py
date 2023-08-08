from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import class_mapper
from exts import db

# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="姓名")
    username = Column(String(50), nullable=False, unique=True, comment="用户名")
    password = Column(String(50), nullable=False, comment="密码")
    telephone = Column(String(50), nullable=False, comment="电话号码")
    role = Column(Integer, nullable=False, comment="0:平台管理员, 1:开发人员")
    token = Column(String(100), comment="验证登录有效性")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    desc = Column(String(100), comment="描述")

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
