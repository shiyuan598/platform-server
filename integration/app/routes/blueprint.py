
def registerRoute(app):
    BASE_URL_PREFIX = "/api"

    # 接口集成
    from .api_process import api_process
    app.register_blueprint(api_process, url_prefix=BASE_URL_PREFIX + "/api_process")

    # 应用集成
    from .app_process import app_process
    app.register_blueprint(app_process, url_prefix=BASE_URL_PREFIX + "/app_process")

    # 项目
    from .project import project
    app.register_blueprint(project, url_prefix=BASE_URL_PREFIX + "/project")

     # 模块
    from .module import module
    app.register_blueprint(module, url_prefix=BASE_URL_PREFIX + "/module")

    # 待办
    from .todo import todo
    app.register_blueprint(todo, url_prefix=BASE_URL_PREFIX + "/todo")

    # 用户
    from .user import user
    app.register_blueprint(user, url_prefix=BASE_URL_PREFIX + "/user")

    # gitlab、jenkins、artifactory
    from .tools import tools
    app.register_blueprint(tools, url_prefix=BASE_URL_PREFIX)
