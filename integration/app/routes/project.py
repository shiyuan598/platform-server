# coding=utf8
# 项目管理
from flask import Blueprint, request, jsonify
from Model import Project, Module, User
from sqlalchemy import func, text, and_, or_, asc, desc, case
from common.utils import generateEntries
from common.artifactory_tool import url as artifactory_base_url
from exts import db
session = db.session

project = Blueprint("project", __name__)

# 项目列表
@project.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        # 查询总数据量
        total = session.query(func.count(Project.id)
        ).join(
            User,
            User.id == Project.owner,
            isouter=True
        ).filter(or_(
            Project.name.like("%{}%".format(name)),
            Project.platform.like("%{}%".format(name)),
            Project.job_name.like("%{}%".format(name)),
            Project.job_name_p.like("%{}%".format(name)),
            Project.job_name_test.like("%{}%".format(name)),
            Project.update_time.like("{}%".format(name)),
            User.name.like("%{}%".format(name))
        )).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Project.id, Project.name, Project.platform, Project.job_name, 
        Project.job_name_p, Project.job_name_test, Project.lidar_path, Project.camera_path, Project.map_path,
        Project.plan_map_path, Project.lidar_point_path, Project.webviz_path, Project.mcu_path, 
        Project.driver_path, Project.sdc_path, Project.owner, User.name.label("owner_name"), Project.desc,
        func.date_format(func.date_add(Project.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Project.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i')
        ).join(
            User,
            User.id == Project.owner,
            isouter=True
        ).filter(or_(
            Project.name.like("%{}%".format(name)),
            Project.platform.like("%{}%".format(name)),
            Project.job_name.like("%{}%".format(name)),
            Project.job_name_p.like("%{}%".format(name)),
            Project.job_name_test.like("%{}%".format(name)),
            Project.update_time.like("{}%".format(name)),
            User.name.like("%{}%".format(name))
        ))

        # 设置排序
        if orderField != "" and orderSeq != "":
            orderField = "project." + orderField
            if orderSeq == "ascend":
                query = query.order_by(asc(text(orderField)))
            else:
                query = query.order_by(desc(text(orderField)))
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "name", "platform", "job_name", "job_name_p", "job_name_test",
            "lidar_path", "camera_path", "map_path", "plan_map_path", "lidar_point_path", "webviz_path", "mcu_path", "driver_path",
            "sdc_path", "owner", "owner_name", "desc", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 所有项目(不分页)
@project.route('/list_all', methods=["GET"])
def search_all():
    try:
        # 查询所有数据
        user_name = request.args.get("user_name")
        query = session.query(Project.id, Project.name, Project.platform, Project.job_name, 
        Project.job_name_p, Project.job_name_test, Project.lidar_path, Project.camera_path, Project.map_path, 
        Project.plan_map_path, Project.lidar_point_path, Project.webviz_path, Project.mcu_path, Project.driver_path, Project.sdc_path,
        func.concat(artifactory_base_url, "/", Project.name, "/cicd/").label("artifacts_url"), 
        func.concat(artifactory_base_url, "/", Project.name, "/user/", user_name, "/").label("artifacts_url_p"), Project.owner)
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "platform", "job_name", "job_name_p", "job_name_test",
            "lidar_path", "camera_path", "map_path", "plan_map_path", "lidar_point_path", "webviz_path", "mcu_path",
            "driver_path", "sdc_path", "artifacts_url", "artifacts_url_p", "owner"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 某项目下的模块列表
@project.route('/<int:project_id>/module', methods=["GET"])
def modules(project_id):
    try:
        # 接收参数
        project_id = request.view_args['project_id']
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "id")
        orderSeq = request.args.get("seq", "")
        # 查询总数据量
        total = session.query(func.count(Module.id)
        ).join(
            User,
            User.id == Module.owner,
            isouter=True
        ).filter(or_(
            Module.name.like("%{}%".format(name)),
            Module.git.like("%{}%".format(name)),
            Module.update_time.like("{}%".format(name)),
            User.name.like("%{}%".format(name))
        )).filter(Module.project == project_id).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Module.id, Module.name, Module.git, Module.owner, User.name.label("owner_name"), Module.desc,
        Module.type, case(
                (Module.type == 0, "基础"),
                (Module.type == 1, "接口"),
                (Module.type == 2, "应用"),
                (Module.type == 3, "配置")
        ).label("type_name"),
        func.date_format(func.date_add(Module.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Module.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i')
        ).join(
            User,
            User.id == Module.owner,
            isouter=True
        ).filter(or_(
            Module.name.like("%{}%".format(name)),
            Module.git.like("%{}%".format(name)),
            Module.update_time.like("{}%".format(name)),
            User.name.like("%{}%".format(name))
        )).filter(Module.project == project_id)

        # 设置排序
        if orderField != "" and orderSeq != "":
            orderField = "module." + orderField
            if orderSeq == "ascend":
                query = query.order_by(asc(text(orderField)))
            else:
                query = query.order_by(desc(text(orderField)))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "name", "git", "owner", "owner_name", "desc", "type", "type_name", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 某项目下的所有模块(不分页)
@project.route('/<int:project_id>/module_all', methods=["GET"])
def modules_all(project_id):
    try:
        # 接收参数
        project_id = request.view_args['project_id']
        types = request.args.getlist("type")
        # 查询所有数据
        query = session.query(Module.id, Module.name, Module.type, Module.git,
            Module.owner, User.name.label("owner_name"), User.telephone.label("owner_phone")
        ).join(
            User,
            User.id == Module.owner,
            isouter=True
        ).filter(Module.project == project_id)
        if len(types) > 0:
            types = tuple(types[0].split(","))
            query = query.filter(Module.type.in_(types))
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "type", "git", "owner", "owner_name", "owner_phone"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 某项目下同一类型的所有模块(不分页)
@project.route('/<int:project_id>/module_type_all/<int:type>', methods=["GET"])
def modules_all_type(project_id, type=0):
    try:
        # 接收参数
        project_id = request.view_args['project_id']
        # 查询所有数据
        query = session.query(Module.id, Module.name, Module.git, Module.owner).filter(
            and_(Module.project == project_id, Module.type == type))
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "git", "owner"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 检查名称是否可用，不存在
@project.route("/check/noexist", methods=["GET"])
def checkExist():
    try:
        name = request.args.get("name")
        total = session.query(func.count(Project.id)).filter(Project.name == name).scalar()
        session.close()
        return jsonify({"code": 0, "data": (total == 0), "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建项目
@project.route('/create', methods=["POST"])
def create():
    try:
        name = request.json.get("name")
        platform = request.json.get("platform")
        job_name = request.json.get("job_name")
        job_name_p = request.json.get("job_name_p")
        job_name_test = request.json.get("job_name_test")
        lidar_path = request.json.get("lidar_path")
        camera_path = request.json.get("camera_path")
        map_path = request.json.get("map_path")
        plan_map_path = request.json.get("plan_map_path")
        lidar_point_path = request.json.get("lidar_point_path")
        webviz_path = request.json.get("webviz_path")
        mcu_path = request.json.get("mcu_path")
        driver_path = request.json.get("driver_path")
        sdc_path = request.json.get("sdc_path")
        owner = request.json.get("owner")
        desc = request.json.get("desc")
        data = Project(name=name, platform=platform,job_name=job_name, job_name_p=job_name_p,
            job_name_test=job_name_test, lidar_path=lidar_path, camera_path=camera_path,
            map_path=map_path, plan_map_path=plan_map_path, lidar_point_path=lidar_point_path, webviz_path=webviz_path,
            mcu_path=mcu_path, driver_path=driver_path, sdc_path=sdc_path, owner=owner, desc=desc)
        session.add(data)
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 编辑项目
@project.route('/edit', methods=["POST"])
def edit():
    try:
        id = request.json.get("id")
        name = request.json.get("name")
        platform = request.json.get("platform")
        job_name = request.json.get("job_name")
        job_name_p = request.json.get("job_name_p")
        job_name_test = request.json.get("job_name_test")
        lidar_path = request.json.get("lidar_path")
        camera_path = request.json.get("camera_path")
        map_path = request.json.get("map_path")
        plan_map_path = request.json.get("plan_map_path")
        lidar_point_path = request.json.get("lidar_point_path")
        webviz_path = request.json.get("webviz_path")
        mcu_path = request.json.get("mcu_path")
        driver_path = request.json.get("driver_path")
        sdc_path = request.json.get("sdc_path")
        owner = request.json.get("owner")
        desc = request.json.get("desc")
        session.query(Project).filter(Project.id == id).update({
            "name": name,
            "platform": platform,
            "job_name": job_name,
            "job_name_p": job_name_p,
            "job_name_test": job_name_test,
            "lidar_path": lidar_path,
            "camera_path": camera_path,
            "map_path": map_path,
            "plan_map_path": plan_map_path,
            "lidar_point_path": lidar_point_path,
            "webviz_path": webviz_path,
            "mcu_path": mcu_path,
            "driver_path": driver_path,
            "sdc_path": sdc_path,
            "owner": owner,
            "desc": desc
        })
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 删除项目--会一并删除项目下的所有模块
@project.route('/delete', methods=["DELETE", "POST"])
def delete():
    try:
        id = request.json.get("id")        
        session.query(Project).filter(Project.id == id).delete()
        session.commit()
        session.close()
        # 删除关联的模块
        session.query(Module).filter(Module.project == id).delete()
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})