```python
from typing import Dict, Tuple, Any, List, Optional
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


# page_data 对应的 Python 代码
class PageDataRequest(BaseModel):
    page: int = Field(..., description="当前页码，从1开始")
    page_size: int = Field(..., description="每页数据条数")
    query: Optional[str] = Field(None, description="查询关键词")


class PageDataItem(BaseModel):
    id: int = Field(..., description="数据项ID")
    name: str = Field(..., description="数据项名称")
    value: str = Field(..., description="数据项值")


class PageDataResponse(BaseModel):
    items: List[PageDataItem] = Field(..., description="当前页的数据列表")
    total: int = Field(..., description="总数据条数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数据条数")


page_data = APIInfo(
    name="page_data",
    describe="分页数据查询",
    url="/data/list",
    method="GET",
    request_model=PageDataRequest,
    response_model=PageDataResponse,
)

###
import datetime

mock_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Mock items for page_data
mock_item_a = dict(id=1, name="Item A", value="Value A")
mock_item_b = dict(id=2, name="Item B", value="Value B")
mock_item_c = dict(id=3, name="Item C", value="Value C")
mock_item_d = dict(id=4, name="Item D", value="Value D")
mock_item_e = dict(id=5, name="Item E", value="Value E")


MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("server_status", "get"): {
        (("keyword", "123456"),): dict(Status="normal", time=mock_time),
        (("keyword", "11222"),): dict(Status="error code", time=mock_time),
        (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    },
    ("page_data", "get"): {
        # Scenario 1: First page, 2 items per page, no query
        (("page", 1), ("page_size", 2), ("query", None)): dict(
            items=[mock_item_a, mock_item_b],
            total=5,
            page=1,
            page_size=2
        ),
        # Scenario 2: Second page, 2 items per page, no query
        (("page", 2), ("page_size", 2), ("query", None)): dict(
            items=[mock_item_c, mock_item_d],
            total=5,
            page=2,
            page_size=2
        ),
        # Scenario 3: Third page, 2 items per page, no query (last item)
        (("page", 3), ("page_size", 2), ("query", None)): dict(
            items=[mock_item_e],
            total=5,
            page=3,
            page_size=2
        ),
        # Scenario 4: First page, 5 items per page, no query (all items)
        (("page", 1), ("page_size", 5), ("query", None)): dict(
            items=[mock_item_a, mock_item_b, mock_item_c, mock_item_d, mock_item_e],
            total=5,
            page=1,
            page_size=5
        ),
        # Scenario 5: Query for "A", first page, 10 items per page
        (("page", 1), ("page_size", 10), ("query", "A")): dict(
            items=[mock_item_a],
            total=1,
            page=1,
            page_size=10
        ),
        # Scenario 6: Query for "C", first page, 10 items per page
        (("page", 1), ("page_size", 10), ("query", "C")): dict(
            items=[mock_item_c],
            total=1,
            page=1,
            page_size=10
        ),
        # Scenario 7: Query for non-existent item, empty result
        (("page", 1), ("page_size", 10), ("query", "NonExistent")): dict(
            items=[],
            total=0,
            page=1,
            page_size=10
        ),
        # Scenario 8: Invalid page number (beyond total pages for given size), empty result
        (("page", 10), ("page_size", 2), ("query", None)): dict(
            items=[],
            total=5, # total still reflects actual total count
            page=10,
            page_size=2
        ),
    }
}
```