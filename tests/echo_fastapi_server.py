#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 13:40
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : echo_fastapi_server.py
import datetime
import inspect
import json
from typing import Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from pydantic import BaseModel

from logistics_api_adk_agent.apis import apis_list
from logistics_api_adk_agent.apis.base import APIInfo

mock_time = datetime.datetime.now().isoformat()
MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("server_status", "get"): {
        (("keyword", "123456"),): dict(Status="normal", time=mock_time),
        (("keyword", "11222"),): dict(Status="error code", time=mock_time),
        (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    }
}

app = FastAPI(title="Dynamic API Server")


def create_dynamic_route(api_metadata: APIInfo):
    """
    根据 APIInfo 动态生成并注册一个 FastAPI 路由函数。
    """
    url: str = api_metadata.url
    method: str = api_metadata.method.lower()
    api_name: str = api_metadata.name
    request_class: Type[BaseModel] = api_metadata.request_model
    response_class: Type[BaseModel] = api_metadata.response_model

    # 1. 构造唯一的函数名
    func_name: str = f"api_{method}_{url.replace('/', '_')}"

    # 2. 动态生成路由处理函数
    # **关键点：** 使用 request_class 作为参数类型注解，FastAPI 会自动处理请求体/查询参数的解析和验证。
    # 对于 GET 请求，request_data 会从查询参数中解析。
    async def dynamic_handler(
        request_data: request_class = Depends(),  # 使用 Depends() 确保 GET 请求的查询参数被正确解析
    ) -> response_class:
        """Dynamic API Handler based on MOCK_DATA lookup."""

        # 3. 查找 MOCK_DATA
        mock_key = (api_name, method)
        mock_entries = MOCK_DATA.get(mock_key, [])

        # 将请求数据转换为字典进行匹配
        request_dict = request_data.model_dump(exclude_none=True)
        request_key = tuple(request_dict.items())
        # 查找匹配的 mock 响应

        matched_response_status = mock_entries.get(request_key)
        if matched_response_status is None:
            raise Exception(f"{func_name} 无参数 {request_dict} 对应的 response")
        # 5. 返回 response_class 实例 (FastAPI 会将其序列化)
        return response_class(**matched_response_status)

    print(f"-> 注册路由: [{method.upper()}] {url}")
    route_decorator = getattr(app, method, None)
    dynamic_handler.__name__ = func_name
    route_decorator(url, response_model=response_class)(dynamic_handler)


for api_def in apis_list:
    create_dynamic_route(api_def)


@app.get("/")
def info():
    return {"message": "Dynamic API Server is running!"}


if __name__ == "__main__":
    # docs http://127.0.0.1:8000/docs
    uvicorn.run(app, host="127.0.0.1", port=8000)
