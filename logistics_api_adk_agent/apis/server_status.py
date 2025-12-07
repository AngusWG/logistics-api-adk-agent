#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 0:56
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : server_status.py
"""demo 测试架构用接口"""
from pydantic import BaseModel, Field
from typing import Type, ClassVar


class StatusRequest(BaseModel):
    keyword: str = Field(..., description="服务器查询密钥")


class StatusResponse(BaseModel):
    Status: str = Field(..., description="服务器状态")
    time: str = Field(..., description="服务器时间")


class ServerStatus(BaseModel):
    # 使用 ClassVar 标记，告诉 Pydantic 这些是类配置，不是模型数据字段
    url: ClassVar[str] = "/status"
    method: ClassVar[str] = "GET"
    # 使用 Type[BaseModel] 或 Type 来注解类属性的类型
    request_class: ClassVar[Type[BaseModel]] = StatusRequest
    response_class: ClassVar[Type[BaseModel]] = StatusResponse
