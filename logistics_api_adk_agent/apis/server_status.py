#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 0:56
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : server_status.py
"""demo 测试架构用接口"""

from pydantic import BaseModel, Field

from logistics_api_adk_agent.apis.base import APIInfo


class StatusRequest(BaseModel):
    keyword: str = Field(..., description="服务器查询密钥")


class StatusResponse(BaseModel):
    Status: str = Field(..., description="服务器状态")
    time: str = Field(..., description="服务器时间")


server_status = APIInfo(
    name="server_status",
    describe="服务器状态查询",
    url="/status",
    method="GET",
    request_model=StatusRequest,
    response_model=StatusResponse,
)
