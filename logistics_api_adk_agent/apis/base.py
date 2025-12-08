#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 13:59
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : base.py
import json
from dataclasses import dataclass
from typing import Callable, Literal, Type

import requests
from pydantic import BaseModel

from logistics_api_adk_agent.config import conf


@dataclass(frozen=True)
class APIInfo:
    name: str
    describe: str
    url: str
    method: Literal["GET", "POST"]
    request_model: Type[BaseModel]
    response_model: Type[BaseModel]

    def create_api_tool_function(self) -> Callable[..., str]:
        """
        作为APIInfo类的实例方法，动态生成一个可调用的Python函数。

        Returns:
            一个符合Gemini Function Calling签名的函数。
        """
        # 从self中提取元数据
        url = self.url
        method = self.method
        request_class = self.request_model

        # response_class = self.response_model # ai会进行处理后返回给用户 所以用不用到这个

        def api_caller(request: request_class) -> str:
            """内部函数，用于实际调用API"""
            full_url = f"{conf.SERVER_BASE_URL}{url}"

            if method.upper() == "POST":
                response = requests.post(
                    full_url,
                    data=request.model_dump_json(),
                    headers={"Content-Type": "application/json"},
                    timeout=5,
                )
            elif method.upper() == "GET":
                response = requests.get(
                    full_url, params=request.model_dump(), timeout=5
                )
            else:
                return json.dumps({"error": f"Unsupported method: {method}"})

            response.raise_for_status()
            return response.text

        api_caller.__name__ = self.name.lower()
        api_caller.__qualname__ = api_caller.__name__

        docstring = f"""
{self.describe}
通过调用 {self.method} {conf.SERVER_BASE_URL}{self.url} API，完成操作。

Args:
    tool_input ({request_class.__name__}): 包含所有请求参数的 Pydantic 模型实例。
        包含字段: {', '.join(request_class.model_fields.keys())}

Returns:
    包含 {self.response_model.__name__} 结构数据的 JSON 字符串。
        """
        api_caller.__doc__ = docstring

        return api_caller
