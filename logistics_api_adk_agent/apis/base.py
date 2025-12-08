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
        response_class = self.response_model

        # 动态构建函数名
        func_name = f"{self.name.lower()}"

        def api_caller(**kwargs) -> str:
            """内部函数，用于实际调用API"""
            try:
                full_url = f"{conf.SERVER_BASE_URL}{url}"

                # 验证和封装请求数据
                request_model_instance = request_class(**kwargs)

                # 转换为JSON负载
                payload = request_model_instance.model_dump_json()

                # 发送请求
                if method.upper() == "POST":
                    response = requests.post(
                        full_url,
                        data=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=5,
                    )
                elif method.upper() == "GET":
                    response = requests.get(full_url, params=kwargs, timeout=5)
                else:
                    return json.dumps({"error": f"Unsupported method: {method}"})

                response.raise_for_status()

                # 返回响应的原始JSON字符串
                return response.text

            except requests.exceptions.RequestException as e:
                error_details = {
                    "error": f"API Error: {e.__class__.__name__}",
                    "details": str(e),
                }
                return json.dumps(error_details)
            except Exception as e:
                error_details = {
                    "error": f"Data Validation Error: {e.__class__.__name__}",
                    "details": str(e),
                }
                return json.dumps(error_details)

        # 设置函数名和文档字符串
        api_caller.__name__ = func_name
        request_fields = []
        for field_name, field_info in request_class.model_fields.items():
            field_type = (
                field_info.annotation.__name__
                if hasattr(field_info.annotation, "__name__")
                else str(field_info.annotation)
            )
            desc = field_info.description or "no description"
            request_fields.append(f"{field_name}: {field_type} (description: {desc})")

        docstring = f"""
{self.describe}
通过调用 {method} {conf.SERVER_BASE_URL}{url} API，完成 {request_class.__name__} 描述的操作。

Args:
    {chr(10).join(['    ' + f for f in request_fields])}

Returns:
    包含 {response_class.__name__} 结构数据的 JSON 字符串。
        """
        api_caller.__doc__ = docstring

        return api_caller
