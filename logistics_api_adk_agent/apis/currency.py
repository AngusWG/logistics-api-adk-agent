#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 18:32
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : currency.py
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from logistics_api_adk_agent.apis.base import APIInfo


# 请求参数模型
class Authorization(BaseModel):
    code: str = Field(..., description="客户编码", min_length=5, max_length=20)
    token: str = Field(..., description="API授权码", min_length=50, max_length=50)


class CurrencyRequest(BaseModel):
    authorization: Authorization = Field(
        ..., description="包含客户编码和授权码的授权信息"
    )


# 响应数据子模型
class CurrencyData(BaseModel):
    code: str = Field(..., description="币别编码")
    cnname: str = Field(..., description="中文名称")
    enname: str = Field(..., description="英文名称")


# 响应数据模型
class CurrencyResponse(BaseModel):
    """
    >>> from logistics_api_adk_agent import run
    >>> res = run("帮我查一下系统可用的币别 code KJHBA token c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas")
    >>> assert "CNY" in res
    >>> assert "港币" in res
    """

    code: int = Field(
        ..., description="接口请求是否通过, 0：表示接口请求通过，其他表示失败"
    )
    msg: str = Field(..., description="说明信息")
    data: List[CurrencyData] = Field(..., description="币别信息列表")


# APIInfo 实例
query_currency = APIInfo(
    name="query_currency",
    describe="查询系统可用的币别",
    url="/api/order/currency",
    method="POST",
    request_model=CurrencyRequest,
    response_model=CurrencyResponse,
)
