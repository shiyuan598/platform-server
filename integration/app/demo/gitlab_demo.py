import gitlab

# 参考：https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html
# https://gitlab.zhito.com/api/v4/projects REST Url 

url = "https://gitlab.zhito.com"
token = "7c5ohyqs1pzL6873cxjd"
gl = gitlab.Gitlab(url=url, private_token=token)

# # 列出所有项目，使用namespace搜索
# projects = gl.projects.list(all=True, simple=True, search_namespaces=True, search="ai/perception_camera")
# for project in projects:
#     print("Project: ", project.name)
#     # 获取分支
#     for branch in project.branches.list():
#         print("\tBranch: ", branch)
#     # print(project, "\n\n")
# # 获取标签
# print("\tTag: ", projects[0].tags.list()[0].name)

# 获取单个项目， 参数：project_name_with_namespace, 
project = gl.projects.get("wangshiyuan/vehicle-resource-server")
print("single project:\n", project, "\n")
print("single project:\n", project.name, "\n")
for branch in project.branches.list():
    print(f"Branch {branch.name}: commit {branch.commit['id']}")

# print("\n********************************************")

# branch = project.branches.get("v1.0")
# print("branch:", branch)
# print("\nbranch v1.0's commit id:", branch.commit["id"])

# commit = ""
# branch_name = "v1.90"
# try:
#     branch = project.branches.get(branch_name)
#     print("branch:", branch)
#     commit = branch.commit["id"]
#     print(f"\nbranch {branch_name}'s commit id: {commit}")
# except gitlab.exceptions.GitlabGetError as e:
#     if e.response_code == 404:
#         tag = project.tags.get(branch_name)
#         commit = tag.commit["id"]
#         print("tag:", tag)
#         print(f"\ntag {branch_name}'s commit id: {commit}")

