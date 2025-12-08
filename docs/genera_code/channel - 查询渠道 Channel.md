``` python
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
import datetime # For mock data, though not strictly used by models
# from logistics_api_adk_agent.apis.base import APIInfo # Assuming this import is available

# Define a placeholder for APIInfo if the actual module is not installed for testing purposes
class APIInfo:
    def __init__(self, name: str, describe: str, url: str, method: str, request_model: BaseModel, response_model: BaseModel):
        self.name = name
        self.describe = describe
        self.url = url
        self.method = method
        self.request_model = request_model
        self.response_model = response_model


class PageDataRequest(BaseModel):
    page_num: int = Field(..., description="当前页码，从1开始")
    page_size: int = Field(..., description="每页数据量")
    keyword: Optional[str] = Field(None, description="可选的查询关键词")


class PageDataResponse(BaseModel):
    total_count: int = Field(..., description="总数据量")
    page_num: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数据量")
    data: List[Dict[str, Any]] = Field(..., description="页面数据列表")


page_data = APIInfo(
    name="page_data",
    describe="分页数据查询",
    url="/page_data",
    method="GET",
    request_model=PageDataRequest,
    response_model=PageDataResponse,
)

###

# MOCK_DATA for testing
# For consistency with the example, we will define a mock_time
mock_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Sample data for pagination responses
sample_item_1 = {"id": 1, "name": "Product A", "price": 10.50}
sample_item_2 = {"id": 2, "name": "Product B", "price": 20.75}
sample_item_3 = {"id": 3, "name": "Product C", "price": 15.00}
sample_item_4 = {"id": 4, "name": "Product D", "price": 5.99}
sample_item_5 = {"id": 5, "name": "Product E", "price": 30.20}
sample_item_6 = {"id": 6, "name": "Product F", "price": 12.30}

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("server_status", "get"): {
        (("keyword", "123456"),): dict(Status="normal", time=mock_time),
        (("keyword", "11222"),): dict(Status="error code", time=mock_time),
        (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    },
    ("page_data", "get"): {
        # Scenario 1: First page, 2 items per page, with keyword "product"
        (("page_num", 1), ("page_size", 2), ("keyword", "product")): dict(
            total_count=6,
            page_num=1,
            page_size=2,
            data=[sample_item_1, sample_item_2]
        ),
        # Scenario 2: Second page, 2 items per page, with keyword "product"
        (("page_num", 2), ("page_size", 2), ("keyword", "product")): dict(
            total_count=6,
            page_num=2,
            page_size=2,
            data=[sample_item_3, sample_item_4]
        ),
        # Scenario 3: Third page, 2 items per page, with keyword "product"
        (("page_num", 3), ("page_size", 2), ("keyword", "product")): dict(
            total_count=6,
            page_num=3,
            page_size=2,
            data=[sample_item_5, sample_item_6]
        ),
        # Scenario 4: First page, 3 items per page, no keyword (keyword=None)
        (("page_num", 1), ("page_size", 3), ("keyword", None)): dict(
            total_count=6,
            page_num=1,
            page_size=3,
            data=[sample_item_1, sample_item_2, sample_item_3]
        ),
        # Scenario 5: Second page, 3 items per page, no keyword (keyword=None)
        (("page_num", 2), ("page_size", 3), ("keyword", None)): dict(
            total_count=6,
            page_num=2,
            page_size=3,
            data=[sample_item_4, sample_item_5, sample_item_6]
        ),
        # Scenario 6: Query with a keyword that yields no results
        (("page_num", 1), ("page_size", 10), ("keyword", "nonexistent")): dict(
            total_count=0,
            page_num=1,
            page_size=10,
            data=[]
        ),
        # Scenario 7: Requesting a page beyond total, still returns empty data for that page
        (("page_num", 10), ("page_size", 5), ("keyword", None)): dict(
            total_count=6, # Total count might still be correct
            page_num=10,
            page_size=5,
            data=[] # But no data for this page
        ),
    }
}
```