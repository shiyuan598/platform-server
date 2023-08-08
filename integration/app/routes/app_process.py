# coding=utf8
# 应用集成
from flask import Blueprint, request, jsonify
from Model import App_process, Project, Process_state, User
from sqlalchemy import func, text, and_, or_, not_, asc, desc
from common.utils import generateEntries
from datetime import datetime, timedelta

from common.jenkins_tool import app_process_log

from .todo import create_todo
from exts import db
session = db.session

app_process = Blueprint("app_process", __name__)

# 应用集成流程列表
@app_process.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "id")
        orderSeq = request.args.get("seq", "descend")
        user_id = int(request.args.get("user_id"))
        user_role = int(request.args.get("user_role"))

        # 获取当前时间和24小时前的时间
        current_time = datetime.now()
        past_time = current_time - timedelta(hours=24)
        # 查询总数据量
        query = session.query(func.count(App_process.id)
        ).join(
            Project,
            App_process.project == Project.id,
            isouter=True
        ).join(
            User,
            User.id == App_process.creator,
            isouter=True
        ).join(
            Process_state,
            App_process.state == Process_state.state,
            isouter=True
        ).filter(or_(
            Project.name.like("%{}%".format(name)),
            App_process.version.like("%{}%".format(name)),
            App_process.desc.like("%{}%".format(name)),
            User.name.like("%{}%".format(name)),
            App_process.create_time.like("{}%".format(name)),
            App_process.update_time.like("{}%".format(name)),
            Process_state.name.like("%{}%".format(name)),
            App_process.api_version.like("%{}%".format(name))
        ))
        # 非管理员，查询系统级的集成流程或自己创建的流程
        # 管理员查询所有的流程
        if user_role != 0:
            query = query.filter(
                or_(App_process.type == 0, App_process.creator == user_id)
            ).filter(
                not_(
                    and_(
                        App_process.state.in_((4, 8)),
                        App_process.create_time < past_time
                    )
                )
            )
        
        total = query.scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(App_process.id, App_process.project, App_process.build_type, App_process.version, App_process.api_version, 
            App_process.lidar, App_process.camera, App_process.map, App_process.job_name, App_process.build_queue, App_process.build_number, 
            App_process.jenkins_url, App_process.artifacts_url, App_process.confluence_url, App_process.test_result_url, App_process.creator,
            User.name.label("creator_name"), App_process.modules, App_process.state,
            Process_state.name.label("state_name"), App_process.type, App_process.desc, 
            Project.name.label("project_name"), Project.lidar_path, Project.camera_path, Project.map_path, Project.plan_map_path,
            Project.lidar_point_path, Project.webviz_path, Project.mcu_path, Project.driver_path, Project.sdc_path,
            App_process.lidar, App_process.camera, App_process.map, App_process.plan_map,
            App_process.lidar_point, App_process.webviz, App_process.mcu, App_process.driver, App_process.sdc, App_process.auto_test,
            func.date_format(func.date_add(App_process.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i:%S'),
            func.date_format(func.date_add(App_process.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i:%S')
        ).join(
            Project,
            App_process.project == Project.id,
            isouter=True
        ).join(
            Process_state,
            App_process.state == Process_state.state,
            isouter=True
        ).join(
            User,
            User.id == App_process.creator,
            isouter=True
        ).filter(or_(
            Project.name.like("%{}%".format(name)),
            App_process.version.like("%{}%".format(name)),
            App_process.desc.like("%{}%".format(name)),
            User.name.like("%{}%".format(name)),
            App_process.create_time.like("{}%".format(name)),
            App_process.update_time.like("{}%".format(name)),
            Process_state.name.like("%{}%".format(name)),
            App_process.api_version.like("%{}%".format(name))
        ))
        # 非管理员，查询系统级的集成流程或自己创建的流程
        # 管理员查询所有的流程
        if user_role != 0:
            query = query.filter(
                or_(App_process.type == 0, App_process.creator == user_id)
            ).filter(
                not_(
                    and_(
                        App_process.state.in_((4, 8)),
                        App_process.create_time < past_time
                    )
                )
            )
        # 设置排序
        if orderField != "" and orderSeq != "":
            orderField = "app_process." + orderField
            if orderSeq == "ascend":
                query = query.order_by(asc(text(orderField)))
            else:
                query = query.order_by(desc(text(orderField)))
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "project", "build_type", "version", "api_version",
            "lidar", "camera", "map", "job_name", "build_queue", "build_number", 
            "jenkins_url", "artifacts_url", "confluence_url", "test_result_url", "creator",
            "creator_name", "modules", "state", "state_name", "type", "desc", 
            "project_name", "lidar_path", "camera_path", "map_path", "plan_map_path",
            "lidar_point_path", "webviz_path", "mcu_path", "driver_path", "sdc_path", "lidar", "camera",
            "map", "plan_map", "lidar_point", "webviz", "mcu", "driver", "sdc", "auto_test", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 检查名称是否可用，不存在
@app_process.route("/version/noexist", methods=["GET"])
def checkExist():
    try:
        project = request.args.get("project")
        creator = request.args.get("creator")
        version = request.args.get("version")
        total = session.query(func.count(App_process.id)).filter(
            and_(
                App_process.project == project,
                App_process.creator == creator,
                App_process.version == version
                )
            ).scalar()
        session.close()
        return jsonify({"code": 0, "data": (total == 0), "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建应用集成
@app_process.route('/create', methods=["POST"])
def create():
    try:
        project = request.json.get("project")
        version = request.json.get("version")
        build_type = request.json.get("build_type")
        auto_test = request.json.get("auto_test")
        desc = request.json.get("desc")
        job_name = request.json.get("job_name")
        modules = request.json.get("modules")
        lidar = request.json.get("lidar")
        camera = request.json.get("camera")
        map = request.json.get("map")
        plan_map = request.json.get("plan_map")
        lidar_point = request.json.get("lidar_point")
        webviz = request.json.get("webviz")
        mcu = request.json.get("mcu")
        driver = request.json.get("driver")
        sdc = request.json.get("sdc")
        creator = request.json.get("creator")
        type = request.json.get("type")
        artifacts_url = request.json.get("artifacts_url")
        state = int(request.json.get("state"))
        data = App_process(project=project, version=version, build_type=build_type,
            auto_test=auto_test, job_name=job_name, lidar=lidar, camera=camera, map=map,
            plan_map=plan_map, lidar_point=lidar_point, webviz=webviz, mcu=mcu, driver=driver, sdc=sdc,
            modules=modules, creator=creator, type=type, artifacts_url=artifacts_url, state=state, desc=desc)
        session.add(data)
        session.flush()
        id = data.id
        session.commit()
        session.close()

        # 系统应用创建待办消息
        if type == 0:
            # 类型：0-接口集成，1-应用集成
            create_todo(type=1, process_id=id, project=project, build_type=build_type, 
                        version=version, creator=creator, desc=desc, modulesStr=modules)
        
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


# 编辑应用集成
@app_process.route('/edit', methods=["POST"])
def edit():
    try:
        id = request.json.get("id")
        project = request.json.get("project")
        version = request.json.get("version")
        build_type = request.json.get("build_type")
        auto_test = request.json.get("auto_test")
        desc = request.json.get("desc")
        job_name = request.json.get("job_name")
        lidar = request.json.get("lidar")
        camera = request.json.get("camera")
        map = request.json.get("map")
        plan_map = request.json.get("plan_map")
        lidar_point = request.json.get("lidar_point")
        webviz = request.json.get("webviz")
        mcu = request.json.get("mcu")
        driver = request.json.get("driver")
        sdc = request.json.get("sdc")
        modules = request.json.get("modules")
        creator = request.json.get("creator")
        type = request.json.get("type")
        state = int(request.json.get("state"))
        session.query(App_process).filter(App_process.id == id).update({
            "project": project,
            "version": version,
            "build_type": build_type,
            "auto_test": auto_test,
            "desc": desc,
            "job_name": job_name,
            "modules": modules,
            "lidar": lidar,
            "camera": camera,
            "map": map,
            "plan_map": plan_map,
            "lidar_point": lidar_point,
            "webviz": webviz,
            "mcu": mcu,
            "driver": driver,
            "sdc": sdc,
            "state": int(state)
        })
        session.commit()
        session.close()

        # 系统应用创建待办消息
        if type == 0:
            # 类型：0-接口集成，1-应用集成
            create_todo(type=1, process_id=id, project=project, build_type=build_type,
                         version=version, creator=creator, desc=desc, modulesStr=modules)
            
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询应用集成中的配置信息
@app_process.route('/info', methods=["GET"])
def modules():
    try:
        id = request.args.get("id")
        result = session.query(App_process.lidar, App_process.camera, 
                               App_process.map, App_process.modules).filter(App_process.id == id).all()
        session.commit()
        session.close()
        data = generateEntries(["lidar", "camera", "map", "modules"], result)
        return jsonify({"code": 0, "data": data[0], "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

@app_process.route('/log', methods=["GET"])
def log():
    try:
        id = request.args.get("id")
        app_process_log(id)
        
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})