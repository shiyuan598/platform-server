# coding=utf8
import datetime
import random
# 用户
from flask import Blueprint, request, jsonify
from Model import User
from sqlalchemy import func, case, text, and_, or_, asc, desc
from common.utils import generateEntries
from exts import db
session = db.session

user = Blueprint("user", __name__)

# 查询所有用户
@user.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "id")
        orderSeq = request.args.get("seq", "ascend")
        # 查询总数据量
        total = session.query(func.count(User.id)).filter(or_(
            User.name.like("%{}%".format(name)),
            User.username.like("%{}%".format(name))
        )).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(User.id, User.name, User.username, User.telephone, User.role,
        case(
                (User.role == 0, "平台管理员"),
                (User.role == 1, "普通用户")
            ).label("role_name")
        ).filter(or_(
            User.name.like("%{}%".format(name)),
            User.username.like("%{}%".format(name))
        ))

        # 设置排序
        if orderField != "" and orderSeq != "":
            orderField = "user." + orderField
            if orderSeq == "ascend":
                query = query.order_by(asc(text(orderField)))
            else:
                query = query.order_by(desc(text(orderField)))
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "name", "username", "telephone", "role", "role_name"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询所有用户，不分页
@user.route('/list/all', methods=["GET"])
def search_all():
    try:
        result = session.query(User.id, User.name, User.username, User.telephone, User.role,
        case(
                (User.role == 0, "平台管理员"),
                (User.role == 1, "普通用户")
            ).label("role_name")
        ).all()
        session.close()
        data = generateEntries(["id", "name", "username", "telephone", "role", "role_name"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 获取不同角色的用户
@user.route('/role/<int:role>', methods=["GET"])
def getUserByRole(role):
    try:
        username = request.args.get("username")
        query = session.query(User.id, User.name, User.username, User.telephone, User.role).filter(User.role == role)
        if username != None:
            query = query.filter(User.username == username)
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "username", "telephone", "role"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建token
def create_token(username):
    try:
        now_time   = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
        random_num = ''.join([str(random.randint(1,9)) for i in range(5)])
        token = now_time + random_num
        result = session.query(User).filter(User.username == username).update({"token": token})
        session.commit()
        session.close()
        if result == 1:
            result = session.query(User.id, User.name, User.username, User.telephone, User.role, User.token
            ).filter(User.username == username).all()
            session.close()
            data = generateEntries(["id", "name", "username", "telephone", "role", "token"], result)
            return jsonify({"code": 0, "data": data, "msg": "成功"})
        return jsonify({"code": 1, "msg": "用户名不存在"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 检查token
def check_token(token):
    try:
        # 检查是否超过时间
        login_time = datetime.datetime.strptime(token[:-5], "%Y%m%d%H%M%S%f")
        interval_time = (datetime.datetime.now() - login_time).seconds
        if interval_time > 8 * 60 * 60:
            return False
        # 检查token是否真实存在
        total = session.query(func.count(User.id)).filter(User.token == token).scalar()
        session.close()
        return total > 0
    except Exception as e:
        session.rollback()
        return False

# 登录方法
def login(username, password):
    try:
        # 检查用户名密码是否正确
        total = session.query(func.count(User.id)).filter(and_(
            User.username == username,
            User.password == password
        )).scalar()
        session.close()
        if total > 0:
            return create_token(username)
        return jsonify({"code": 1, "msg": "用户名或密码错误"}) 
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 用户登录
@user.route('/login', methods=["POST"])
def route_login():
    try:
        username = request.json.get("username")
        password = request.json.get("password")
        return login(username, password)
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 添加用户
def addUser(username, password, role, name, telephone):
    try:
        data = User(username=username, password=password, role=role, name=name, telephone=telephone)
        session.add(data)
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 添加用户--管理员添加用户
@user.route('/add', methods=["POST"])
def add():
    try:
        name = request.json.get("name")
        username = request.json.get("username")
        password = request.json.get("password")
        telephone = request.json.get("telephone")
        role = request.json.get("role")
        return addUser(username, password, role, name, telephone)
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 编辑用户
@user.route('/update', methods=["POST"])
def update():
    try:
        id = request.json.get("id")
        name = request.json.get("name")
        password = request.json.get("password")
        telephone = request.json.get("telephone")
        role = request.json.get("role")
        result = session.query(User).filter(User.id == id).update({
            "name": name,
            "password": password,
            "telephone": telephone,
            "role": role
        })
        session.commit()
        session.close()
        if result == 1:
            return jsonify({"code": 0, "msg": "成功"})
        return jsonify({"code": 1, "msg": "要编辑的用户不存在"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 删除用户
@user.route('/delete', methods=["POST", "DELETE"])
def delete():
    try:
        id = request.json.get("id")        
        session.query(User).filter(User.id == id).delete()
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 检查用户名是否可用，不存在
@user.route("/check/noexist", methods=["GET"])
def checkExist():
    try:
        username = request.args.get("username")
        total = session.query(func.count(User.id)).filter(User.username == username).scalar()
        session.close()
        return jsonify({"code": 0, "data": (total == 0), "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 检查用户名信息是否正确
@user.route("/check/correct", methods=["GET"])
def checkCorrect():
    try:
        username = request.args.get("username")
        telephone = request.args.get("telephone")
        total = session.query(func.count(User.id)).filter(and_(
            User.username == username,
            User.telephone == telephone
        )).scalar()
        session.close()
        return jsonify({"code": 0, "data": (total > 0), "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 用户注册
@user.route('/register', methods=["POST"])
def register():
    try:
        name = request.json.get("name")
        username = request.json.get("username")
        password = request.json.get("password")
        telephone = request.json.get("telephone")
        role = request.json.get("role")
        res = addUser(username, password, role, name, telephone)
        if res.json["code"] != 0:
            return res
        return login(username, password)
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 重置密码
@user.route('/resetpwd', methods=["POST"])
def resetPassword():
    try:
        username = request.json.get("username")
        password = request.json.get("password")
        telephone = request.json.get("telephone")
        result = session.query(User).filter(and_(
            User.username == username,
            User.telephone == telephone
        )).update({
            "username": username,
            "password": password,
            "telephone": telephone
        })
        session.commit()
        session.close()
        if result == 1:
            return login(username, password)
        return jsonify({"code": 1, "msg": "用户名信息错误"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})