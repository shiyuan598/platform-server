from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import class_mapper
from exts import db

# 项目
class Project(db.Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="名称", unique=True)
    platform = Column(String(50), nullable=False, comment="平台")
    job_name = Column(Text, nullable=False, comment="jenkins构建任务的名称")
    job_name_p = Column(Text, nullable=False, comment="jenkins构建个人任务的名称")
    job_name_test = Column(Text, nullable=False, comment="jenkins构建测试任务的名称")
    lidar_path = Column(Text, nullable=False, comment="激光模型的存放路径")
    camera_path = Column(Text, nullable=False, comment="视觉模型的存放路径")
    map_path = Column(Text, nullable=False, comment="地图数据的存放路径")
    plan_map_path = Column(Text, nullable=False, comment="规划地图数据的存放路径")
    lidar_point_path = Column(Text, nullable=False, comment="点云地图数据的存放路径")
    webviz_path = Column(Text, nullable=False, comment="webviz的存放路径")
    mcu_path = Column(Text, nullable=False, comment="mcu的存放路径")
    driver_path = Column(Text, nullable=True, comment="驱动的存放路径")
    sdc_path = Column(Text, nullable=True, comment="SDC的存放路径")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    owner = Column(Integer, nullable=False, comment="负责人")
    desc = Column(String(200), comment="描述")

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c) 
