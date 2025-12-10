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
    """
    >>> from logistics_api_adk_agent import run
    >>> # 成功查询的场景
    >>> res_success = run("帮我查一下渠道信息 code KJHBA token 60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas")
    >>> assert "CN_EMS" in res_success
    >>> assert "中国邮政" in res_success
    >>> assert "香港TNT" in res_success
    >>> # 授权失败的场景
    >>> res_auth_fail = run("帮我查一下渠道信息 code ERROR token invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    >>> assert "授权失败" in res_auth_fail
    >>> assert "1001" in res_auth_fail
    >>> # 参数校验失败的场景 (token 长度不足)
    >>> res_param_fail = run("帮我查一下渠道信息 code KJHBA token short")
    >>> assert "请求参数校验失败" in res_param_fail
    >>> assert "token长度不足50" in res_param_fail
    """

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
