import jenkins

jenkins_server_url = "https://jenkins.zhito.com"
user_id = "wangshiyuan"
api_token = "11bdffee022bd22472efdf2ebd99354522"
server=jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token, timeout=10)
job = "Integration/HWL4_AARCH64_PERSONAL"

parameters = {
    "project": "HWL4_ORIN",
    "version": "v0.24-test",
    "build_type": "Release",
    "user": "admin",
    "timestamp": "20230712-113013",
    "config": {
        "config_parameter": {
            "url": "git@gitlab.zhito.com:ai/config_parameter.git",
            "branch": "zhito-sweep"
        },
        "truck_parameter": {
            "url": "git@gitlab.zhito.com:ai/truck_parameter.git",
            "branch": "main"
        }
    },
    "base": {
        "message_group": {
            "url": "git@gitlab.zhito.com:ai/message_group.git",
            "branch": "zhito-l4-dev"
        }
    },
    "modules": {},
}

# 构建job
# build_id = server.build_job(job, parameters)
# build_id = server.build_job(job)
# print("\nbuild_id: ", build_id) #16581

# 创建job
# server.create_job(job, config_xml=config_xml)

# 获取job配置，job名需要包含路径
# config = server.get_job_config(job)
# print(config)

# job_info = server.get_job_info(job)
# print("\njob_info:", job_info)

# # 查询下一次build的number
# nextBuildNumber = server.get_job_info(job)['nextBuildNumber']
# print("\nextBuildNumber: ", nextBuildNumber)

# 构建job
# build_id = server.build_job(job, parameters)
# build_id = server.build_job(job)
# print("\nbuild_id: ", build_id) #16581

# item = server.get_queue_item(number=build_id)
# print("\nqueue item:", item)

# # 查询job最后一次build的number
# build_number = server.get_job_info(job)['lastBuild']['number']
# print("\nbuild_number: ", build_number)

# # 查询build状态及结果
# build_info = server.get_build_info(job, 9, depth=0)
# print("\nbuild_info:", build_info["result"], build_info["queueId"], build_info["url"], "\n\n", build_info)
# print("\n\n: ", build_info["duration"], build_info["progress"])

# # 查询stage
# stage_info = server.get_build_stages(job, 9)
# print("\nstage_info:\n", stage_info)


#  办法：
#  1.build前假定该次build_number = nextBuildNumber, 记录queueId
#  2.查询build_info前, 先查询lastbuildNumber, 
#    2.1 lastBuildNumber < build_number, 直接返回, 认为build进行中, 需要等一会再查询
#    2.2 lastBuildNumber >= build_number时, 查询buildInfo
#    2.3 比较buildInfo.queueId和记录的queueId
#    2.4 如果相等,返回buildInfo
#    2.5 如果不相等, build_number = build_number + 1, 重复执行步骤2
#  tips:build之后不能立即查询到build_number,等待时间不确定

# nextBuildNumber = server.get_job_info(job)['nextBuildNumber']
# print("\nnext_build_number：", nextBuildNumber)
# build_info = server.get_build_info(job, nextBuildNumber)
# print("\nbuild_info:", build_info["result"], build_info["queueId"], build_info["url"], build_info["url"])


# build_info = server.get_build_info(job, 59)
# print("\n\n", build_info, "\n\n")
# print("\nbuild_info:", build_info["result"], build_info["queueId"], build_info["url"])