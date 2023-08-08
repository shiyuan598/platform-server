# coding=utf8
# 工具接口，gitlab/jenkins/artifactory/confluence
import datetime, json
from flask import Blueprint, request, jsonify
from common.gitlab_tool import getAllBranches, getAllTags, multiGetBranchesTags
from common.jenkins_tool import build
from common.artifactory_tool import getAllFiles, getAllFolders, getUri
from common.redis_tool import redis_get, redis_set
from Model import Api_process, App_process
from exts import db
session = db.session

tools = Blueprint("tools", __name__)

# 拉取gitlab分支
@tools.route('/gitlab/branch', methods=["GET"])
def branch():
    try:
        project = request.args.get("project_name_with_namespace", "")
        data = getAllBranches(project)
        return jsonify({"code": 0, "data": {"branch": data}, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab的Tag
@tools.route('/gitlab/tag', methods=["GET"])
def tag():
    try:
        project = request.args.get("project_name_with_namespace", "")
        data = getAllTags(project)
        return jsonify({"code": 0, "data": {"tag": data}, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab多个项目的分支和Tag
@tools.route('/gitlab/multiple/branch_tag', methods=["GET"])
def branch_tag():
    try:
        # 获取参数：
        projects = request.args.getlist("projects")
        project_names = projects[0].split(",")
        use_cache = request.args.get("cache", "true")

        # 从redis缓存中查询
        cache_result = {} # 缓存中取的值
        nocache_result = {} # 通过接口查询的值
        nocache_project = [] # 缓存中没有值的项目名称
        if use_cache == "true":
            for project_name in project_names:
                cache_data = redis_get(project_name)
                if cache_data != None:
                    # 缓存中有就使用缓存数据
                    cache_result[project_name] = json.loads(cache_data.decode("utf-8"))
                    print(f"\n从**缓存**中获取到{project_name}的数据\n")
                else:
                    # 缓存中没有就记录下项目名称一起查询
                    print(f"\n从**接口**中查询{project_name}的数据\n")
                    nocache_project.append(project_name)
        else:
            nocache_project = project_names
        # 没有缓存的就通过api查询，并更新到缓存中
        if len(nocache_project) > 0:
            nocache_result = multiGetBranchesTags(nocache_project)
            for key, value in nocache_result.items():
                res = redis_set(key, json.dumps(value).encode("utf-8"))
                print(f"\n设置缓存{key}, {res}\n")
        # 把两种方式获取的数据合并
        data = {**cache_result, **nocache_result}
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 触发jenkins构建
@tools.route('/jenkins/build_job', methods=["POST"])
def build_job():
    try:
        process_type = int(request.json.get("process_type"))
        process_id = int(request.json.get("process_id"))
        job = request.json.get("job")
        artifacts_url = request.json.get("artifacts_url")
        parameters = request.json.get("parameters")
        data = build(job, {"param": parameters})
        # 更新集成流程中的build_number, build_queue
        if process_type == 0:
            session.query(Api_process).filter(Api_process.id == process_id).update({           
                "build_number": data["build_number"],
                "build_queue": data["build_queue"],
                "artifacts_url": artifacts_url,
                "state": 2 # 进行中
            })
            session.commit()
            session.close()
        else:
            if process_type == 1:
                session.query(App_process).filter(App_process.id == process_id).update({           
                    "build_number": data["build_number"],
                    "build_queue": data["build_queue"],
                    "artifacts_url": artifacts_url,
                    "state": 2 # 进行中
                })
                session.commit()
                session.close()
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询artifactory目录下的文件
@tools.route('/artifacts/files', methods=["GET"])
def artifacts_files():
    try:
        path = request.args.get("path", "")
        if path == "":
            data = []
        else:
            data = getAllFiles(path)

        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})
    
# 查询artifactory目录下的文件
@tools.route('/artifacts/folders', methods=["GET"])
def artifacts_folders():
    try:
        path = request.args.get("path", "")
        if path == "":
            data = []
        else:
            data = getAllFolders(path)

        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 查询artifactory目录的访问URI
@tools.route('/artifacts/uri', methods=["GET"])
def artifacts_uri():
    try:
        path = request.args.get("path", "GSL2/test/x86/1.0.0")
        data = getUri(path)

        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 短信状态回调
@tools.route('/sms/callback', methods=["POST"])
def callback():
    try:
        mobile = request.json[0].get("mobile")
        user_receive_time = request.json[0].get("user_receive_time")
        report_status = request.json[0].get("report_status")
        errmsg = request.json[0].get("errmsg")
        description = request.json[0].get("description")
        sid = request.json[0].get("sid")
        print("\n短信下发状态：\n当前时间：{}, 手机号：{}, 接收时间：{}, 状态：{}, 错误消息：{}, 描述：{}, SID：{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mobile, user_receive_time, report_status, errmsg, description, sid), flush=True)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        print("短信下发状态错误：", str(e), flush=True)
        return jsonify({"code": 1, "msg": str(e)})