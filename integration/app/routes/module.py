# coding=utf8
# 模块管理
from flask import Blueprint, request, jsonify
from Model import Project, Module
from sqlalchemy import func, and_
from exts import db
session = db.session

module = Blueprint("module", __name__)

# 检查名称是否可用，不存在
@module.route("/check/noexist", methods=["GET"])
def checkExist():
    try:
        project = request.args.get("project")
        name = request.args.get("name")
        type = request.args.get("type")
        total = session.query(func.count(Module.id)).filter(and_(
            Module.project == project, Module.name == name, Module.type == type)).scalar()
        session.close()
        return jsonify({"code": 0, "data": (total == 0), "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建模块
@module.route('/create', methods=["POST"])
def create():
    try:
        project = request.json.get("project")
        name = request.json.get("name")
        type = request.json.get("type")
        git = request.json.get("git")
        owner = request.json.get("owner")
        desc = request.json.get("desc")
        data = Module(project=project, name=name, type=type, git=git, owner=owner, desc=desc)
        session.add(data)
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

#编辑模块
@module.route('/edit', methods=["POST"])
def edit():
    try:
        id = request.json.get("id")
        name = request.json.get("name")
        type = request.json.get("type")
        git = request.json.get("git")
        owner = request.json.get("owner")
        desc = request.json.get("desc")
        session.query(Module).filter(Module.id == id).update({
            "name": name,
            "type": type,
            "git": git,
            "owner": owner,
            "desc": desc
        })
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 删除模块
@module.route('/delete', methods=["DELETE", "POST"])
def delete():
    try:
        id = request.json.get("id")        
        session.query(Module).filter(Module.id == id).delete()
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})