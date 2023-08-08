import json
import jenkins
from Model import Api_process, App_process, Project, Process_state, User
from sqlalchemy import func, text, and_
from exts import db
from config.setting import JENKINS
from common.utils import generateEntries, get_url_param_value
from .confluence_tool import create_page, get_or_create_page_by_title, append_page_by_id
session = db.session

jenkins_server_url = JENKINS["jenkins_server_url"]
user_id = JENKINS["user_id"]
api_token = JENKINS["api_token"]
server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token, timeout=10)

# 构建job
def build(job, parameters):
    try:
        # 查询下一次build的number
        nextBuildNumber = server.get_job_info(job)['nextBuildNumber']

        # 构建job
        build_queue = server.build_job(job, parameters)
        return {
            "build_number": nextBuildNumber,
            "build_queue": build_queue
        }
    except Exception as e:
        print('An exception occurred in jenkins build ', str(e), flush=True)

# 更新任务状态
def update_build_state(data, type="Api_process"):
    try:
        update_ids = [] # 更新数据的Id
        for item in data:
            id = item[0]
            job_name = item[1]
            build_number = item[2]
            build_queue = item[3]
            jenkins_url = item[5]
            auto_test = item[6]
            platform = item[7]
            # 获取jenkins构建信息
            info = query_build_info(job_name, build_number, build_queue)
            if info != None:
                # 单更新url, jenkins_url为空时更新
                if (info["state"] == 2 and info["jenkins_url"] != None and (jenkins_url == None or jenkins_url == "")):
                    if type == "Api_process":
                        session.query(Api_process).filter(Api_process.id == id).update({
                            "jenkins_url": info["jenkins_url"]
                        })
                        session.commit()
                        session.close()
                    if type == "App_process":
                        session.query(App_process).filter(App_process.id == id).update({
                            "jenkins_url": info["jenkins_url"]
                        })
                        session.commit()
                        session.close()
                    # 记录变化的数据id
                    update_ids.append(id)
                # 更新url和状态
                if (info["state"] > 2):
                    if type == "Api_process":
                        session.query(Api_process).filter(Api_process.id == id).update({
                            "state": info["state"],
                            "jenkins_url": info["jenkins_url"]
                        })
                        session.commit()
                        session.close()
                    if type == "App_process":
                        test_result_url = "";
                        if auto_test == 1 and platform == "ORIN":
                            parts = job_name.split('/')
                            parts.insert(1, 'job')
                            new_job_name = '/'.join(parts)
                            test_result_url = f'https://jenkins.zhito.com/job/{new_job_name}/{info["number"]}/test_5fresult_5fonline/;https://jenkins.zhito.com/job/{new_job_name}/{info["number"]}/test_5fresult_5foffline/'
                        session.query(App_process).filter(App_process.id == id).update({
                            "state": info["state"],
                            "jenkins_url": info["jenkins_url"],
                            "test_result_url": test_result_url
                        })
                        session.commit()
                        session.close()
                        # 写confluence日志
                        app_process_log(id)
                        # 构建成功的开始自动化测试
                        if info["state"] == 3:
                            run_auto_test(id)
                    update_ids.append(id) # 记录变化的数据id
    except Exception as e:
        session.rollback()
        print('An exception occurred at update_build_state ', str(e), flush=True)

#  办法：
#  1.build前假定该次build_number = nextBuildNumber, 记录queueId
#  2.查询build_info前, 先查询lastbuildNumber, 
#    2.1 lastBuildNumber < build_number, 直接返回, 认为build进行中, 需要等一会再查询
#    2.2 lastBuildNumber >= build_number时, 查询buildInfo
#    2.3 比较buildInfo.queueId和记录的queueId
#    2.4 如果相等,返回buildInfo
#    2.5 如果不相等, build_number = build_number + 1, 重复执行步骤2
#  tips:build之后不能立即查询到build_number,等待时间不确定

# 查询job状态
def query_build_info(job, build_number, build_queue):
    try:
        # 查询job最后一次build的number, 判断当前能否查询到
        last_build_number = server.get_job_info(job)['lastBuild']['number']
        if last_build_number < build_number:
            # 目前还查询不到
            return {
                "state": 2,
                "jenkins_url": None,
                "number": build_number
            }
        else:
            # 查询build_info, 比对queue
            build_info = server.get_build_info(job, build_number)
            # 相等时, 认为是这个build
            if build_queue == build_info["queueId"]:
                # 未构建结束，更新url
                if build_info["result"] == None:
                    return {
                        "state": 2,
                        "jenkins_url": build_info["url"],
                        "number": build_info["number"]
                    }
                else:
                    # 构建结束，更新结果、状态
                    return {
                        "state": 3 if build_info["result"].lower() == "success" else 4,
                        "jenkins_url": build_info["url"],
                        "number": build_info["number"]
                    }
            # 否则认为是下一次构建
            else:
                return query_build_info(job, build_number + 1, build_queue)
    except Exception as e:
        print('An exception occurred in get_build_info ', str(e), flush=True)

# 向confluence中写入构建日志
def app_process_log(id):
    try:
        # 查询本次构建的参数信息
        result = session.query(Project.name.label("project_name"), App_process.version, App_process.build_type,
            App_process.jenkins_url, App_process.artifacts_url, User.username.label("username"),
            User.name.label("creator_name"), App_process.modules, Process_state.name.label("state_name"), 
            App_process.desc, func.date_format(func.date_add(App_process.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
            Project.lidar_path, Project.camera_path, Project.map_path, App_process.lidar, App_process.camera,
            App_process.map, App_process.confluence_url, App_process.test_result_url
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
            ).filter( # 查询系统级的集成流程
                and_(App_process.type == 0, App_process.id == id)
            ).all()
        session.close()
        if len(result) > 0:
            data = generateEntries(["project_name", "version", "build_type", "jenkins_url", "artifacts_url", "username",
            "creator_name", "modules", "state_name", "desc", "create_time", "lidar_path", "camera_path", "map_path",
            "lidar", "camera", "map", "confluence_url", "test_result_url"], result)[0]
            project_name = data["project_name"]
            version = data["version"]
            build_type = data["build_type"]
            desc = data["desc"]
            jenkins_url = data["jenkins_url"]
            artifacts_url = data["artifacts_url"]
            creator_name = data["creator_name"]
            state_name = data["state_name"]
            create_time = data["create_time"]
            modulesStr = data["modules"]
            lidar_model = f"{data['lidar_path'].rstrip('/')}/{ data['lidar'].lstrip('/')}" if data['lidar'] != None else ""
            camera_model = f"{data['camera_path'].rstrip('/')}/{ data['camera'].lstrip('/')}" if data['camera'] != None else ""
            map_data = f"{data['map_path'].rstrip('/')}/{ data['map'].lstrip('/')}" if data['map'] != None else ""
            test_result_url = data["test_result_url"]
            module_config = generator_build_config(project_name=project_name, version=version, build_type=build_type,
                modulesStr=modulesStr, lidar_model=lidar_model, camera_model=camera_model, map_data=map_data)
            # 获取父页面id
            parent_page_id = get_or_create_page_by_title(project_name + "【应用】", type="App_process")
            # 标题
            title = f"{version}【{create_time[0: 10]}】【应用】"
            # 内容
            content = f'<p>项目：{project_name}</p>\
            <p>版本号：{version}</p>\
            <p>集成类型：应用集成</p>\
            <p>描述：{desc}</p>\
            <p>创建人：{creator_name}</p>\
            <p>时间：{create_time}</p>\
            <p>结果：{state_name}</p>\
            <p>Jenkins:&nbsp;<a class="external-link" style="text-decoration: none;" href="{jenkins_url}" rel="nofollow">{jenkins_url}</a></p>\
            <p>Artifacts:&nbsp;<a class="external-link" style="text-decoration: none;" href="{artifacts_url}" rel="nofollow">{artifacts_url}</a></p>\
            <p>模块配置信息：</p>\
            <ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="06dba324-f02c-4410-8fa5-190d5d7f8bcd">\
            <ac:plain-text-body><![CDATA[{module_config}]]></ac:plain-text-body>\
            </ac:structured-macro><p class="auto-cursor-target"><br /></p>'
            
            if test_result_url != None:
                urls = test_result_url.split(";")
                url_str = "<p>自动化测试：</p>"
                for item in urls:
                    url_str = url_str + f'<a class="external-link" style="text-decoration: none;" href="{item}" rel="nofollow">{item}</a><br/>'
                
                content = content + url_str
            # 生成confluence页面
            result = create_page(title=title, content=content, parent_page_id=parent_page_id)
            # 把页面地址写人库中
            session.query(App_process).filter(App_process.id == id).update({
                "confluence_url": result["url"]
            })
            session.commit()
            session.close()
    except Exception as e:
        print('An exception occurred in app_process_log ', str(e), flush=True)

# 生成构建的配置参数
def generator_build_config(project_name, version, build_type, modulesStr, lidar_model, camera_model, map_data):
    try:
        modules = json.loads(modulesStr)
        config = {}
        base = {}
        common = {}
        for item, value in modules.items():
            if value["type"] == 3:
                config[item] = {
                    "url": value["url"],
                    "branch": value["version"],
                }
            elif value["type"] == 0:
                base[item] = {
                    "url": value["url"],
                    "branch": value["version"],
                }
            elif value["type"] == 2:
                common[item] = {
                    "url": value["url"],
                    "branch": value["version"],
                    "owner": value["owner_name"],
                    "release_note": value["release_note"]
                }
        
        result = {
            "project": project_name,
            "version": version,
            "build_type": build_type,
            "lidar_model": lidar_model,
            "camera_model": camera_model,
            "map_data": map_data,
            "config": config,
            "base": base,
            "modules": common
        }
        return json.dumps(result, indent=4, ensure_ascii=False)
    except Exception as e:
        print('An exception occurred in generator_build_config ', str(e), flush=True)

# 定时任务，查询build状态
def schedule_task():
    try:
        print("\n", "schedule_task", flush=True)
        # 待更新状态的数据
        appProcessData = session.query(App_process.id, App_process.job_name, App_process.build_number, App_process.build_queue,
                App_process.type, App_process.jenkins_url, App_process.auto_test, Project.platform
            ).join(
                Project,
                App_process.project == Project.id,
                isouter=True
            ).filter(App_process.state == 2).all()
        session.close()
        update_build_state(appProcessData, "App_process")
        # 更新自动化测试的进度
        appProcessData = session.query(App_process.id, Project.job_name_test, App_process.build_number,
                App_process.build_queue, App_process.version, App_process.confluence_url,
                func.date_format(func.date_add(App_process.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i')
            ).join(
                Project,
                App_process.project == Project.id,
                isouter=True
            ).filter(App_process.state == 6).all()
        session.close()
        update_test_build_state(appProcessData)
    except Exception as e:
        print('An exception occurred in schedule_task ', str(e), flush=True)

# 运行自动化测试
def run_auto_test(id):
    try:
        print("\n开始自动化测试")
        result = session.query(App_process.id, App_process.auto_test, Project.job_name_test, App_process.artifacts_url
        ).join(
                Project,
                App_process.project == Project.id,
                isouter=True
        ).filter(and_(App_process.auto_test == 1, App_process.id == id, Project.job_name_test != None)).all()
        session.close()
        if len(result) > 0:
            data = generateEntries(["id", "auto_test", "job_name_test", "artifacts_url"], result)[0]
            
            build_info = build(data["job_name_test"], {"package_path": data["artifacts_url"].lstrip("https://artifactory.zhito.com/artifactory/")})
            session.query(App_process).filter(App_process.id == id).update({           
                    "build_number": build_info["build_number"],
                    "build_queue": build_info["build_queue"],
                    "state": 6 # 测试中
                })
            session.commit()
            session.close()
    except Exception as e:
        print('An exception occurred in app_process_log ', str(e), flush=True)

# 更新测试任务状态
def update_test_build_state(data):
    try:
        for item in data:
            id = item[0]
            job_name = item[1]
            build_number = item[2]
            build_queue = item[3]
            version = item[4]
            confluence_url = item[5]
            create_time = item[6]
            # 获取jenkins构建信息
            info = query_build_info(job_name, build_number, build_queue)
            if info != None:
                if info["state"] > 2:
                    # 测试结果url
                    # 将'Integration/HWL4_X86_Integration_Test' ==> 'Integration/job/HWL4_X86_Integration_Test'
                    parts = job_name.split('/')
                    parts.insert(1, 'job')
                    new_job_name = '/'.join(parts)
                    test_result_url = f'https://jenkins.zhito.com/job/{new_job_name}/{info["number"]}/test_5fresult/'
                    # 更新测试状态后结果url
                    session.query(App_process).filter(App_process.id == id).update({
                        "test_result_url": test_result_url if info["state"] == 3 else "",
                        "state": 7 if info["state"] == 3 else 8 # 测试中
                    })
                    session.commit()
                    session.close()

                    # 测试完成后更新confluence
                    if info["state"] == 3:
                        page_id =  get_url_param_value(confluence_url, "pageId")
                        if page_id != "":
                            title = f"{version}【{create_time[0: 10]}】【应用】"                        
                            content = f'<p>Auto Test:&nbsp;<a class="external-link" style="text-decoration: none;" href="{test_result_url}" rel="nofollow">{test_result_url}</a></p>'
                            append_page_by_id(page_id, title, content)                   

    except Exception as e:
        session.rollback()
        print('An exception occurred at update_build_state ', str(e), flush=True)