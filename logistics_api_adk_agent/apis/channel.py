#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 18:30
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : channel.py

from datetime import datetime
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, Field

from logistics_api_adk_agent.apis.base import APIInfo


# 请求参数模型
class Authorization(BaseModel):
    code: str = Field(..., description="客户编码", min_length=5, max_length=20)
    token: str = Field(..., description="API授权码", min_length=50, max_length=50)


class ChannelRequest(BaseModel):
    authorization: Authorization = Field(
        ..., description="包含客户编码和授权码的授权信息"
    )


# 响应数据子模型
class ChannelData(BaseModel):
    channelid: str = Field(..., description="渠道代码")
    channeltype: str = Field(..., description="渠道类型")
    channelname: str = Field(..., description="渠道简称")
    channelnamecn: str = Field(..., description="渠道中文名称")
    channelnameen: str = Field(..., description="渠道英文名称")


# 响应数据模型
class ChannelResponse(BaseModel):
    code: int = Field(
        ..., description="接口请求是否通过, 0：表示接口请求通过，其他表示失败"
    )
    msg: str = Field(..., description="说明信息")
    data: List[ChannelData] = Field(..., description="渠道信息列表")


# APIInfo 实例
query_channel = APIInfo(
    name="query_channel",
    describe="查询渠道信息",
    url="/api/order/channel",
    method="POST",
    request_model=ChannelRequest,
    response_model=ChannelResponse,
)
