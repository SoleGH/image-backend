from common.utils import logger
import os
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import dashscope


class Wanxiang:
    """通义万相图像合成服务封装，提供文生图、图生图等能力的通用调用入口"""

    def __init__(self, api_url='https://maas.qianwenaiapi.com/api/v1'):
        # 设置 dashscope 的 API 基础地址
        dashscope.base_http_api_url = api_url

    def image_synthesis(self, prompt, model="wanx-x-painting", task="image2image",
                        base_image_url=None, mask_image_url=None,
                        n=1, size='1024*1024', save_dir='./'):
        """
        同步调用通义万相进行图像合成，并将生成的图片下载到本地

        :param prompt: 图像生成的提示词
        :param model: 使用的模型名称，默认为 wanx-x-painting
        :param task: 任务类型，如 text2image（文生图）、image2image（图生图）
        :param base_image_url: 图生图任务的底图 URL，image2image 时必传
        :param mask_image_url: 图生图任务的遮罩图 URL，image2image 时必传
        :param n: 生成图片的数量
        :param size: 生成图片的尺寸，格式如 '1024*1024'
        :param save_dir: 生成图片的本地保存目录，默认为当前目录
        :return: 成功返回生成图片的 URL 列表，失败返回 None
        """
        # 图生图任务校验必传参数
        if task == 'image2image':
            if not base_image_url or not mask_image_url:
                raise ValueError("image2image 任务必须传入 base_image_url 和 mask_image_url")

        # 根据任务类型组装 extra_input
        extra_input = {}
        if task == 'image2image':
            extra_input['base_image_url'] = base_image_url
            extra_input['mask_image_url'] = mask_image_url

        logger.debug('----sync call, please wait a moment----')
        rsp = ImageSynthesis.call(model=model,
                                  prompt=prompt,
                                  n=n,
                                  size=size,
                                  task=task,
                                  extra_input=extra_input)
        if rsp.status_code == HTTPStatus.OK:
            urls = []
            # 遍历生成结果，下载并保存到本地
            for result in rsp.output.results:
                urls.append(result.url)
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                save_path = os.path.join(save_dir, file_name)
                with open(save_path, 'wb+') as f:
                    f.write(requests.get(result.url).content)
            return urls
        else:
            logger.error('sync_call Failed, status_code: %s, code: %s, message: %s' %
                  (rsp.status_code, rsp.code, rsp.message))
            return None


# 万相图像合成服务单例，供其他模块直接导入使用
wanxiang_client = Wanxiang()
