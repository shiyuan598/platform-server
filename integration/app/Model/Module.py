from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import class_mapper
from exts import db

# 模块
class Module(db.Model):
    __tablename__ = 'module'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(Integer, nullable=False, comment="项目")
    name = Column(String(50), nullable=False, comment="名称")
    type = Column(Integer, nullable=False, server_default="0", comment="模块类型，0：base，1：接口集成，2：应用集成，3：配置")
    git = Column(String(200), nullable=False, comment="git")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    owner = Column(Integer, nullable=False, comment="负责人")
    desc = Column(String(200), comment="描述")
    __table_args__ = (UniqueConstraint('name', 'project', 'type', name='uq_name_project_type'),) # 同一个项目下同一类型的模块名不能重复

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c) 
