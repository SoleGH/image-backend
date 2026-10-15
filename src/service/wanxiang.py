from setting import settings
from common.utils import logger
import os
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message, ImageGenerationResponse


class Wanxiang:
    """通义万相图像合成服务封装，提供文生图、图生图等能力的通用调用入口"""

    def __init__(self, api_url='https://maas.qianwenaiapi.com/api/v1'):
        # 设置 dashscope 的 API 基础地址
        dashscope.base_http_api_url = api_url
        dashscope.api_key = settings.wanxiang_api_key

    def image_synthesis(self, prompt, base_image_url=None, save_dir='./'):
        """
        同步调用通义万相进行图像合成，并将生成的图片下载到本地
        https://platform.qianwenai.com/docs/developer-guides/image-generation/wan-image-editing
        """
        # 图生图任务校验必传参数
        # if task == 'image2image':
        #     if not base_image_url or not mask_image_url:
        #         raise ValueError("image2image 任务必须传入 base_image_url 和 mask_image_url")

        message = Message(
            role="user",
            content=[
                {
                    "text": prompt,
                },
                {
                    "image": base_image_url
                }
            ]
        )

        logger.debug('----sync call, please wait a moment----')
        rsp = ImageGeneration.call(
            model='wan2.7-image-pro',
            api_key=settings.wanxiang_api_key,
            messages=[message],
            watermark=False,
            n=1,
            size="2K"
        )

        if hasattr(rsp, 'status_code') and rsp.status_code == HTTPStatus.OK:
            urls = []
            # 遍历生成结果，下载并保存到本地
            for result in rsp.output.choices:  # rsp.output.choices[0].message.content[0]['image']
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
