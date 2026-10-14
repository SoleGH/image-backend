from flask_restful import Resource, reqparse

from common import utils
from common.utils import logger, BaseCustomException


class PathViewV1(Resource):
    _path_prefix = "/api/v1"
    _path = None  # "/api/v1/path_view_v1"

    @classmethod
    @property
    def path(cls):
        if not hasattr(cls, "_path") or not cls._path:
            # 如果没有配置则自动根据类名生成
            return f"{cls._path_prefix}/{utils.to_lower_camel_case(cls.__name__)}"
        else:
            return cls._path

    def dispatch_request(self, *args, **kwargs):
        try:
            # todo: 校验登录状态和权限
            
            # 然后调用真正的方法：get/post/put等
            return super().dispatch_request(*args, **kwargs)
        except BaseCustomException as e:
            return {"message": str(e)}, e.status_code
        except Exception as e:
            logger.exception(e)
            return {"message": "服务器内部错误"}, 500

    @classmethod
    def response_success_dict(cls, **kwargs):
        """生成单个成功响应字典
        返回包含 status='success' 及任意附加字段的字典与 200 状态码
        """
        temp = dict(status='success')
        if kwargs:
            temp.update(**kwargs)
        return temp, 200

    @classmethod
    def response_success_list(cls, result_list, total=None, **kwargs):
        """生成列表成功响应字典
        返回包含 status='success'、count、result 及任意附加字段的字典与 200 状态码
        参数:
            result_list: 列表数据
            total: 总数，不传则使用 result_list 长度
            **kwargs: 附加字段
        """
        temp = {
            "status": "success",
            "count": total if total is not None else len(result_list),
            "result": result_list
        }
        if kwargs:
            temp.update(**kwargs)
        return temp, 200

    @classmethod
    def response_error(cls, message, status_code=400):
        """生成错误响应字典
        返回包含 status='error' 及错误信息的字典与指定状态码
        参数:
            message: 错误信息
            status_code: HTTP 状态码，默认 400
        """
        return {
            "status": 'error',
            "message": message,
        }, status_code

    @classmethod
    def parse_page(cls):
        """解析分页参数
        返回偏移量和每页数量
        """
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, required=False, default=1, location='args')
        parser.add_argument('page_size', type=int, required=False, default=10, location='args')
        data = parser.parse_args()

        offset = (data['page'] - 1) * data['page_size'] if data['page'] >= 1 else 0
        return offset, data['page_size']
