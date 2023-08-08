# coding=utf8
# 待办
import re, json
from flask import Blueprint, request, jsonify
from Model import Todo, Project, App_process, User
from sqlalchemy import func, text, or_, asc, desc, case
from sqlalchemy.orm import aliased
from common.utils import generateEntries
from common.sms import sendMessage
from exts import db
session = db.session

todo = Blueprint("todo", __name__)

# 待办列表
@todo.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        orderField = request.args.get("order", "id")
        orderSeq = request.args.get("seq", "")
        filter = request.args.get("state", 0)
        user_id = int(request.args.get("user_id"))
        # 查询总数据量
        query = session.query(func.count(Todo.id)).filter(or_(Todo.creator == user_id, Todo.handler == user_id))
        if filter != "":
            query = query.filter(Todo.state == int(filter))
        
        total = query.scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 表别名，便于多次join同一个表
        S = aliased(User)
        T = aliased(User)
        # 查询分页数据
        query = session.query(Todo.id, Todo.type, Todo.process_id, Todo.project, Project.name.label("project_name"), 
            Todo.build_type, Todo.version, Todo.module_name, Todo.creator, S.name.label("creator_name"), Todo.handler, 
            T.name.label("handler_name"), T.telephone.label("handler_phone"), Todo.desc, 
            (func.TIMESTAMPDIFF(text("MINUTE"), Todo.prompt_time, func.now()) > 60).label("enable_prompt"),
            func.date_format(func.date_add(Todo.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
            func.date_format(func.date_add(Todo.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
            case(
                (Todo.type == 0, "接口集成"),
                (Todo.type == 1, "应用集成")
            ).label("type_name")
        ).join(
            Project,
            Todo.project == Project.id,
            isouter=True
        ).join(
            S,
            Todo.creator == S.id,
            isouter = True
        ).join(
            T,
            Todo.handler == T.id,
            isouter = True
        )
        query = query.filter(or_(Todo.creator == user_id, Todo.handler == user_id))
        if filter != "": # 查询历史待办
            query = query.filter(Todo.state == int(filter))

        # 设置排序
        if orderField != "" and orderSeq != "":
            orderField = "todo." + orderField
            if orderSeq == "ascend":
                query = query.order_by(asc(text(orderField)))
            else:
                query = query.order_by(desc(text(orderField)))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "type", "process_id", "project", "project_name", "build_type",
        "version", "module_name", "creator", "creator_name", "handler", "handler_name", "handler_phone", 
        "desc", "enable_prompt", "create_time", "update_time", "type_name"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建待办消息, 类型：0-接口集成，1-应用集成
def create_todo(type, process_id, project, build_type, version, creator, desc, modulesStr):
    try:
      modules = json.loads(modulesStr)
      # 删除之前的待办消息
      session.query(Todo).filter(Todo.process_id == process_id).delete()
      session.commit()
      session.close()
      for key, value in modules.items():
        # base模块不需要创建待办, 填写过version的不需要创建待办
        if value["type"] != 0 and value["version"] == "":
            data = Todo(type=type, process_id=process_id, project=project, build_type=build_type,
                version=version, creator=creator, desc=desc, module_name=key, handler=value["owner"])
            session.add(data)
            session.commit()
            session.close()
            # 通知模块负责人
            phone = value["owner_phone"]
            if check_phone_number(phone):
                sendMessage(TemplateId="1773455", PhoneNumberSet=['+86' + phone])
    except Exception as e:
        session.rollback()
        print('An exception occurred at create_todo', str(e), flush=True)

# 处理待办消息
@todo.route('/handle', methods=["POST"])
def handle_todo():
    try:
        type = request.json.get("type")# 类型：0-接口集成，1-应用集成
        id = request.json.get("id")
        process_id = request.json.get("process_id")
        module_name = request.json.get("module_name")
        version = request.json.get("version")
        release_note = request.json.get("release_note")
        # 1.更新 *应用* 集成流程的模块信息及状态
        if type == 1:
            update_app_process_module(process_id, module_name, version, release_note)
        # 2.更新待办消息的状态
        session.query(Todo).filter(Todo.id == id).update({"state": 1})
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        print('An exception occurred at handle_todo', str(e), flush=True)
        return jsonify({"code": 1, "msg": str(e)})

# 更新应用集成的模块
def update_app_process_module(id, module_name, version, release_note):
    try:
        result = session.query(App_process.modules, User.name, User.telephone).join(
            User,
            User.id == App_process.creator,
            isouter=True
        ).filter(App_process.id == id).all()
        modules = json.loads(result[0]["modules"])
        modules[module_name]["version"] = version
        modules[module_name]["release_note"] = release_note
        keys = modules.keys()
        state = 1
        # 所有模块信息填写完整后状态为已就绪
        for key in keys:
            if modules[key]["version"] == "":
                state = 0
        session.query(App_process).filter(App_process.id == id).update({
            "modules": json.dumps(modules, indent=4),
            "state": state
        })
        session.commit()
        session.close()
        # 短信通知流程发起人
        phone = result[0]["telephone"]
        if check_phone_number(phone):
            sendMessage(TemplateId="1773476", PhoneNumberSet=['+86' + phone])
        return True
    except Exception as e:
        session.rollback()
        return False

# 催办待办消息
@todo.route('/prompt', methods=["POST"])
def prompt_todo():
    try:
        type = request.json.get("type") # 类型：0-接口集成，1-应用集成
        id = request.json.get("id")
        project_name = request.json.get("project_name")
        version = request.json.get("version")
        module_name = request.json.get("module_name")
        phone = request.json.get("phone")
        # 更新待办消息的prompt_time
        session.query(Todo).filter(Todo.id == id).update({"prompt_time": func.now()})
        session.commit()
        session.close()
        # 发送短信
        if check_phone_number(phone):
            sendMessage(TemplateId="1773455", PhoneNumberSet=['+86' + phone])
        return jsonify({"code": 0, "data": True, "msg": "成功"})
    except Exception as e:
        session.rollback()
        print('An exception occurred at handle_todo', str(e), flush=True)
        return jsonify({"code": 1, "msg": str(e)})

# 检查号码是否有效
def check_phone_number(phone):
    pattern = '^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1589]))\d{8}$'
    res = re.match(pattern, phone)
    return (res != None)
