#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 13:40
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : echo_fastapi_server.py
import datetime
import inspect
import json
from functools import wraps
from typing import Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type, Union

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request
from mock_data import MOCK_DATA
from pydantic import BaseModel

from logistics_api_adk_agent.apis import apis_list
from logistics_api_adk_agent.apis.base import APIInfo

app = FastAPI(title="Dynamic API Server")


def recursive_dict_to_sorted_tuple(
    data: Union[Dict, List, Any],
) -> Union[Tuple, List, Any]:
    """
    递归地将字典转换为排序后的元组，以便用于查找 MOCK_DATA。

    Args:
        data: 要转换的数据（可能是 dict, list, 或其他 Any）。

    Returns:
        转换后的数据 (tuple, list, 或其他 Any)。
    """
    if isinstance(data, dict):
        # 1. 对字典的键进行排序 (确保顺序一致)
        sorted_items = sorted(data.items())
        # 2. 递归处理每个值
        converted_items = []
        for key, value in sorted_items:
            # 键必须是字符串，值需要递归转换
            converted_items.append((key, recursive_dict_to_sorted_tuple(value)))
        # 3. 将结果转换为元组
        return tuple(converted_items)

    elif isinstance(data, list):
        # 递归处理列表中的每个元素
        return tuple((recursive_dict_to_sorted_tuple(item) for item in data))

    else:
        # 其他类型（如 int, float, str, None, bool）保持不变
        return data


def create_dynamic_route(api_metadata: APIInfo):
    """
    根据 APIInfo 动态生成并注册一个 FastAPI 路由函数。
    """
    url: str = api_metadata.url
    method: str = api_metadata.method.lower()
    api_name: str = api_metadata.name
    request_class: Type[BaseModel] = api_metadata.request_model
    response_class: Type[BaseModel] = api_metadata.response_model

    func_name: str = f"api_{method}_{url.replace('/', '_')}"

    if method in ["post", "put", "patch"]:

        param_default = Body(..., embed=False)
    else:
        # 使用 Depends() 来解析查询参数 (GET)
        param_default = Depends()

    def signature_decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)
        new_param = inspect.Parameter(
            name="request_data",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=param_default,
            annotation=request_class,
        )
        new_sig = sig.replace(parameters=[new_param])

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.__signature__ = new_sig
        wrapper.__name__ = func_name
        return wrapper

    @signature_decorator
    async def dynamic_handler(request_data) -> response_class:
        """Dynamic API Handler based on MOCK_DATA lookup."""

        mock_key = (api_name, method)
        print("=" * 20)
        print(f"  - get access: {mock_key}")
        # print(f"request data: {request_data}")
        print(f"  - request json data: {request_data.model_dump_json()}")
        mock_entries = MOCK_DATA.get(mock_key, [])

        request_dict = request_data.model_dump(exclude_none=True)
        request_key = recursive_dict_to_sorted_tuple(request_dict)

        matched_response_status = mock_entries.get(request_key)
        print(f"  - matched_response_status: {matched_response_status}")

        if matched_response_status is None:
            matched_response_status = [i for i in mock_entries.values()][0]
            print(f"  - 未找到数据 匹配第一个数据: {matched_response_status}")
            # raise (f"{func_name} 无参数 {request_dict} 对应的 response")

        return response_class(**matched_response_status)

    print(f"-> 注册路由: [{method.upper()}] {url}")
    route_decorator = getattr(app, method, None)
    # dynamic_handler.__name__ = func_name
    route_decorator(url, response_model=response_class)(dynamic_handler)


for api_def in apis_list:
    create_dynamic_route(api_def)


@app.get("/")
def info():
    return {"message": "Dynamic API Server is running!"}


if __name__ == "__main__":
    # docs http://127.0.0.1:8000/docs
    uvicorn.run(app, host="127.0.0.1", port=8000)
