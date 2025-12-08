```python
from pydantic import BaseModel, Field
from logistics_api_adk_agent.apis.base import APIInfo
from typing import List, Dict, Any, Tuple
import datetime

# Pydantic Models for PageDataRequest
class PageDataRequest(BaseModel):
    page_num: int = Field(1, description="当前页码，默认为1")
    page_size: int = Field(10, description="每页大小，默认为10")


# Pydantic Models for PageDataResponse
class PageDataResponse(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="页面数据列表")
    total_count: int = Field(..., description="总条目数")
    page_num: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")


# APIInfo for page_data
page_data = APIInfo(
    name="page_data",
    describe="获取分页数据",
    url="/page_data",
    method="GET",
    request_model=PageDataRequest,
    response_model=PageDataResponse,
)

###
# 生成对应的测试用例
mock_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("server_status", "get"): {
        (("keyword", "123456"),): dict(Status="normal", time=mock_time),
        (("keyword", "11222"),): dict(Status="error code", time=mock_time),
        (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    },
    ("page_data", "get"): {
        # 场景1: 不传入任何参数，使用默认值 (page_num=1, page_size=10)
        ((),): dict(
            data=[{"id": 1, "name": "Item A", "value": 100}, {"id": 2, "name": "Item B", "value": 101}],
            total_count=25,
            page_num=1,
            page_size=10
        ),
        # 场景2: 传入特定的 page_num 和 page_size
        (("page_num", 2), ("page_size", 5)): dict(
            data=[{"id": 6, "name": "Item F", "value": 105}, {"id": 7, "name": "Item G", "value": 106}, {"id": 8, "name": "Item H", "value": 107}],
            total_count=25,
            page_num=2,
            page_size=5
        ),
        # 场景3: 只传入 page_num，page_size 使用默认值 (10)
        (("page_num", 3),): dict(
            data=[{"id": 21, "name": "Item U", "value": 120}, {"id": 22, "name": "Item V", "value": 121}],
            total_count=30, # 模拟不同的总数
            page_num=3,
            page_size=10
        ),
        # 场景4: 只传入 page_size，page_num 使用默认值 (1)
        (("page_size", 20),): dict(
            data=[{"id": i, "name": f"Big Item {i}", "value": 200 + i} for i in range(1, 5)],
            total_count=50,
            page_num=1,
            page_size=20
        ),
        # 场景5: 请求的页码超出总数据范围，返回空数据
        (("page_num", 10), ("page_size", 10)): dict(
            data=[],
            total_count=25,
            page_num=10,
            page_size=10
        ),
    }
}
```