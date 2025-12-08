from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Any
from datetime import datetime

# 请求参数模型
class Authorization(BaseModel):
    code: str = Field(..., description="客户编码", min_length=5, max_length=20)
    token: str = Field(..., description="API授权码", min_length=50, max_length=50)

class ChannelRequest(BaseModel):
    authorization: Authorization = Field(..., description="包含客户编码和授权码的授权信息")

# 响应数据子模型
class ChannelData(BaseModel):
    channelid: str = Field(..., description="渠道代码")
    channeltype: str = Field(..., description="渠道类型")
    channelname: str = Field(..., description="渠道简称")
    channelnamecn: str = Field(..., description="渠道中文名称")
    channelnameen: str = Field(..., description="渠道英文名称")

# 响应数据模型
class ChannelResponse(BaseModel):
    code: int = Field(..., description="接口请求是否通过, 0：表示接口请求通过，其他表示失败")
    msg: str = Field(..., description="说明信息")
    data: List[ChannelData] = Field(..., description="渠道信息列表")

# APIInfo 实例
query_channel = APIInfo(
    name="query_channel",
    describe="查询渠道信息",
    url="http://www.cntodd.top//api/order/channel",
    method="POST",
    request_model=ChannelRequest,
    response_model=ChannelResponse,
)

###

mock_time = datetime.now().isoformat()
MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("query_channel", "post"): {
        (
            ("authorization", (("code", "KJHB"), ("token", "c60bf762-01f7-470e-8c8f-acde06c81fed"))),
        ): dict(
            code=0,
            msg="调用成功",
            data=[
                {"channelid": "CN_EMS", "channeltype": "快递", "channelname": "中国邮政", "channelnamecn": "中国邮政", "channelnameen": "China Post"},
                {"channelid": "HK_TNT", "channeltype": "专线", "channelname": "香港TNT", "channelnamecn": "香港TNT", "channelnameen": "Hong Kong TNT"},
                {"channelid": "MS_KQ", "channeltype": "专线", "channelname": "美森快船", "channelnamecn": "美森快船", "channelnameen": "Mason Clippers"},
            ],
        ),
        (
            ("authorization", (("code", "ERROR"), ("token", "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"))),
        ): dict(
            code=1001,
            msg="授权失败，请检查code和token",
            data=[],
        ),
        (
            ("authorization", (("code", "KJHB"), ("token", "short"))),
        ): dict(
            code=400,
            msg="请求参数校验失败：token长度不足50",
            data=[],
        ),
    }
}