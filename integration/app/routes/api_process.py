# coding=utf8
# 接口集成
from flask import Blueprint, request, jsonify
from Model import Api_process, Project, Process_state, User
from sqlalchemy import func, text, or_, asc, desc
from common.utils import generateEntries
from exts import db
session = db.session

api_process = Blueprint("api_process", __name__)

# 接口集成流程列表
@api_process.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "id")
        orderSeq = request.args.get("seq", "")
        user_id = request.args.get("user_id")
        # 查询总数据量
        total = session.query(func.count(Api_process.id)).filter(or_(
            Api_process.project.like("%{}%".format(name)),
            Api_process.version.like("%{}%".format(name)),
            Api_process.release_note.like("%{}%".format(name))
        )).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Api_process.id, Api_process.project, Api_process.build_type, Api_process.version, Api_process.release_note,
        Api_process.job_name, Api_process.build_queue, Api_process.build_number, Api_process.jenkins_url, Api_process.artifacts_url, Api_process.confluence_url,
        Api_process.creator, User.name.label("creator_name"), Api_process.modules, Api_process.state, Process_state.name.label("state_name"), Api_process.desc, Project.name.label("project_name"),
        func.date_format(func.date_add(Api_process.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Api_process.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        ).join(
            Project,
            Api_process.project == Project.id,
            isouter=True
        ).join(
            Process_state,
            Api_process.state == Process_state.state,
            isouter=True
        ).join(
            User,
            User.id == Api_process.creator,
            isouter=True
        ).filter(or_(
            Api_process.project.like("%{}%".format(name)),
            Api_process.version.like("%{}%".format(name)),
            Api_process.release_note.like("%{}%".format(name))
        ))

        # 设置排序
        if orderField != "" and orderSeq != "":
            orderField = "api_process." + orderField
            if orderSeq == "ascend":
                query = query.order_by(asc(text(orderField)))
            else:
                query = query.order_by(desc(text(orderField)))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "project", "build_type", "version", "release_note", "job_name", "build_queue", "build_number",
        "jenkins_url", "artifacts_url", "confluence_url", "creator", "creator_name", "modules", "state", "state_name", "desc", "project_name", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建接口集成
@api_process.route('/create', methods=["POST"])
def create():
    try:
        project = request.json.get("project")
        version = request.json.get("version")
        build_type = request.json.get("build_type")
        release_note = request.json.get("release_note")
        job_name = request.json.get("job_name")
        modules = request.json.get("modules")
        creator = request.json.get("creator")
        artifacts_url = request.json.get("artifacts_url")
        data = Api_process(project=project, version=version, build_type=build_type, release_note=release_note, 
        job_name=job_name, modules=modules, creator=creator, artifacts_url=artifacts_url)
        session.add(data)
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


# 编辑接口集成
@api_process.route('/edit', methods=["POST"])
def edit():
    try:
        id = request.json.get("id")
        project = request.json.get("project")
        version = request.json.get("version")
        build_type = request.json.get("build_type")
        release_note = request.json.get("release_note")
        job_name = request.json.get("job_name")
        modules = request.json.get("modules")
        state = request.json.get("state")
        session.query(Api_process).filter(Api_process.id == id).update({
            "project": project,
            "version": version,
            "build_type": build_type,
            "release_note": release_note,
            "job_name": job_name,
            "modules": modules,
            "state": int(state)
        })
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


# 更新接口集成中的模块配置
@api_process.route('/update_module', methods=["POST"])
def update_module():
    try:
        id = request.json.get("id")
        modules = request.json.get("modules")
        state = request.json.get("state")
        session.query(Api_process).filter(Api_process.id == id).update({           
            "modules": modules,
            "state": int(state) # 所有模块信息填写完整后状态为已就绪
        })
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})
