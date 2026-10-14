import inspect

from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from common.utils import logger

from setting import settings

from view.hello import *

app = Flask(__name__)


app.config['SECRET_KEY'] = settings.flask_secret_key  # session 密钥
api = Api(app)


class Alive(Resource):
    @staticmethod
    def get():
        return "alive!"


def register_routes():
    route_list = [(Alive,'/alive')]
    views = [view for view in PathViewV1.__subclasses__()]  # 自动获取所有views
    # for i in [User, Login, Logout, AddUser]:
    for i in views:
        file_path = inspect.getfile(i)
        code_line = inspect.getsourcelines(i)[1]

        path = i.path
        logger.debug(f"Add route:{path}, File {file_path}:{code_line}")
        route_list.append((i, path))
    for route in route_list:
        api.add_resource(*route)


def main():
    register_routes()

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(settings.server_port)
    logger.info(f"Server start at:{settings.server_port}")

    # 开启多线程,但start需要调用os.fork()函数,windows下os没有该函数
    # http_server.bind(5000)
    # http_server.start(0)

    IOLoop.instance().start()

"""
单进程:
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()

+++++++++++++++++++++++++++++
多进程
http_server = HTTPServer(WSGIContainer(app))
# 开启多线程,但start需要调用os.fork()函数,windows下os没有该函数
# http_server.bind(5000)
# http_server.start(0)  # 指定fork子进程数量

IOLoop.instance().start()

+++++++++++++++++++++++++++++
高级多进程
sockets = tornado.netutil.bind_sockets(8888)
tornado.process.fork_processes(0)
server = HTTPServer(app)
server.add_sockets(sockets)
IOLoop.current().start()
"""

if __name__ == '__main__':
    # 开发环境使用Flask内置服务器并开启热重载
    if settings.debug:
        register_routes()
        app.run(debug=True, use_reloader=True, port=settings.server_port,
                threaded=False, passthrough_errors=True)
    else:
        main()
