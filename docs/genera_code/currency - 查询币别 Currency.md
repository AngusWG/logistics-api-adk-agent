from pydantic import BaseModel, Field, conlist
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime

# 请求参数模型
class Authorization(BaseModel):
    code: str = Field(..., description="客户编码", min_length=5, max_length=20)
    token: str = Field(..., description="API授权码", min_length=50, max_length=50)

class CurrencyRequest(BaseModel):
    authorization: Authorization = Field(..., description="包含客户编码和授权码的授权信息")

# 响应数据子模型
class CurrencyData(BaseModel):
    code: str = Field(..., description="币别编码")
    cnname: str = Field(..., description="中文名称")
    enname: str = Field(..., description="英文名称")

# 响应数据模型
class CurrencyResponse(BaseModel):
    code: int = Field(..., description="接口请求是否通过, 0：表示接口请求通过，其他表示失败")
    msg: str = Field(..., description="说明信息")
    data: List[CurrencyData] = Field(..., description="币别信息列表")

# APIInfo 实例
query_currency = APIInfo(
    name="query_currency",
    describe="查询系统可用的币别",
    url="http://www.cntodd.top//api/order/currency",
    method="POST",
    request_model=CurrencyRequest,
    response_model=CurrencyResponse,
)

###

mock_time = datetime.now().isoformat()
MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("query_currency", "post"): {
        (
            ("authorization", (("code", "KJHBA"), ("token", "60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"))),
        ): dict(
            code=0,
            msg="调用成功",
            data=[
                {"code": "CNY", "cnname": "人民币", "enname": "CNY"},
                {"code": "HKG", "cnname": "港币", "enname": "HKD"},
                {"code": "USD", "cnname": "美元", "enname": "USD"},
                {"code": "EUR", "cnname": "欧元", "enname": "EUR"},
                {"code": "GBP", "cnname": "英镑", "enname": "GBP"},
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
            ("authorization", (("code", "KJHBA"), ("token", "short"))),
        ): dict(
            code=400,
            msg="请求参数校验失败：token长度不足50",
            data=[],
        ),
    }
}
