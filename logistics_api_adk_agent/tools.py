#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:02
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : tools.py
import json
from typing import Type, Callable

import requests
from pydantic import BaseModel

import logistics_api_adk_agent.apis
BASE_URL = "http://127.0.0.1:8000"

def create_api_tool_function(api_metadata_class: Type[BaseModel]) -> Callable[..., str]:
    """
    根据 API 元数据类（包含 URL, METHOD, Request Class）动态生成一个可调用的 Python 函数。

    Args:
        api_metadata_class: 包含 API 端点信息的 Pydantic 类（如 CreateShipmentAPI）。

    Returns:
        一个符合 Gemini Function Calling 签名 (接受参数，返回 JSON 字符串) 的函数。
    """

    url = api_metadata_class.url
    method = api_metadata_class.method
    request_class = api_metadata_class.request_class

    # 动态构建函数名
    func_name = api_metadata_class.__name__

    # ----------------------------------------------------------------------
    # 步骤 1: 构建动态函数 (使用 exec 或 type() 创建，但闭包更简单且可读)
    # ----------------------------------------------------------------------

    def api_caller(**kwargs) -> str:
        """
        这个内部函数就是最终返回的、用于调用外部 API 的函数。
        它捕获了外部作用域中的 url, method, request_class 变量。
        """
        try:
            full_url = f"{BASE_URL}{url}"

            # 使用 Request Model 来验证和构造 payload
            # **注意**: kwargs 中包含的参数必须与 request_class 的字段匹配

            # 1. 验证和封装请求数据
            request_model_instance = request_class(**kwargs)

            # 2. 将模型转换为 JSON 负载
            payload = request_model_instance.model_dump_json()

            # 3. 发送请求
            if method.upper() == "POST":
                response = requests.post(full_url, data=payload, headers={'Content-Type': 'application/json'},
                                         timeout=5)
            elif method.upper() == "GET":
                # 对于 GET 请求，通常参数在 URL 或 query 中，这里简单起见，我们假设 GET 不需要复杂 JSON Body
                # 但由于 request_class 存在，我们仍使用 kwargs 构建 payload 作为请求体（虽然不标准，但保持通用性）
                response = requests.get(full_url, params=kwargs, timeout=5)
            else:
                return json.dumps({"error": f"Unsupported method: {method}"})

            response.raise_for_status()

            # 4. 返回 API 响应的原始 JSON 字符串
            return response.text

        except requests.exceptions.RequestException as e:
            error_details = {"error": f"API Error: {e.__class__.__name__}", "details": str(e)}
            return json.dumps(error_details)
        except Exception as e:
            error_details = {"error": f"Data Validation Error: {e.__class__.__name__}", "details": str(e)}
            return json.dumps(error_details)

    api_caller.__name__ = func_name
    # 尝试设置 Docstring 和注解（这是最难的部分，通常需要第三方库或 Python 3.10+ 的 inspect.signature）
    # 在这里我们简化，手动设置 Docstring
    request_fields = ", ".join([f"{k}: {v.__class__.__name__}" for k, v in request_class.model_fields.items()])
    docstring = f"""
        通过调用 {method} {url} API，完成 {request_class.__name__} 描述的操作。

        Args:
            {request_fields}

        Returns:
            包含 {api_metadata_class.response_class.__name__} 结构数据的 JSON 字符串。
        """
    api_caller.__doc__ = docstring
    return api_caller

# 最终工具集
AVAILABLE_FUNCTIONS = {}
TOOL_LIST = []

print("--- 动态生成 API 工具函数 ---")
for api_meta in logistics_api_adk_agent.apis.apis_list:
    # 调用包装器创建新的函数
    new_func = create_api_tool_function(api_meta)

    # 注册到字典和列表
    AVAILABLE_FUNCTIONS[new_func.__name__] = new_func
    TOOL_LIST.append(new_func)

    print(f"  ✅ 生成函数: {new_func.__name__}")

# ------------------------------------
# 验证和使用 (演示如何像 create_new_shipment 一样调用)
# ------------------------------------
print("\n--- 验证生成的工具 ---")

# 1. 访问第一个工具（对应 CreateShipmentAPI）
shipment_tool = AVAILABLE_FUNCTIONS['ServerStatus']

# 验证函数名称和 Docstring
print(f"函数名: {shipment_tool.__name__}")
print("--- Docstring ---")
print(shipment_tool.__doc__.strip())