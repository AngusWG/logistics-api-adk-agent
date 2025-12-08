```python
from typing import List, Dict, Tuple, Any, Optional
from pydantic import BaseModel, Field
# 假设 APIInfo 从现有模块导入
from logistics_api_adk_agent.apis.base import APIInfo


# page_data 的请求模型
class PageDataRequest(BaseModel):
    page: int = Field(1, description="当前页码，默认为1")
    page_size: int = Field(10, description="每页返回的条目数，默认为10")
    keyword: Optional[str] = Field(None, description="查询关键字，可选")


# page_data 列表中的单个数据项模型
class PageDataItem(BaseModel):
    id: str = Field(..., description="数据项唯一标识")
    title: str = Field(..., description="数据项标题")
    content: str = Field(..., description="数据项内容摘要")
    created_at: str = Field(..., description="创建时间，ISO格式字符串")


# page_data 的响应模型
class PageDataResponse(BaseModel):
    items: List[PageDataItem] = Field(..., description="当前页的数据列表")
    total: int = Field(..., description="总数据条数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")


# page_data 的 APIInfo 配置
page_data_api = APIInfo(
    name="get_page_data",
    describe="分页查询数据",
    url="/page_data",
    method="GET",
    request_model=PageDataRequest,
    response_model=PageDataResponse,
)

###
# 测试数据（Mock Data）
# 导入 datetime 用于生成 mock_time，如果需要的话
from datetime import datetime
# mock_time = datetime.now().isoformat() # 如果 server_status 需要，可以保留

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    # 如果原始的 server_status 数据也需要包含在这里，可以添加
    # ("server_status", "get"): {
    #     (("keyword", "123456"),): dict(Status="normal", time=mock_time),
    #     (("keyword", "11222"),): dict(Status="error code", time=mock_time),
    #     (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    # },
    ("get_page_data", "get"): {
        # 测试用例1: 默认页码和大小，无关键字
        (("page", 1), ("page_size", 10)): {
            "items": [
                {"id": "item_001", "title": "新闻标题A", "content": "这是第一篇新闻的摘要内容。", "created_at": "2023-01-01T10:00:00"},
                {"id": "item_002", "title": "通知公告B", "content": "这是第二篇公告的摘要内容。", "created_at": "2023-01-01T10:05:00"},
                {"id": "item_003", "title": "科技前沿C", "content": "这是第三篇科技文章的摘要内容。", "created_at": "2023-01-01T10:10:00"},
                {"id": "item_004", "title": "生活小贴士D", "content": "这是第四篇生活贴士的摘要内容。", "created_at": "2023-01-01T10:15:00"},
                {"id": "item_005", "title": "产品更新E", "content": "这是第五篇产品更新的摘要内容。", "created_at": "2023-01-01T10:20:00"},
            ],
            "total": 25, # 假设总共有25条数据
            "page": 1,
            "page_size": 10,
        },
        # 测试用例2: 第二页，每页5条，无关键字
        (("page", 2), ("page_size", 5)): {
            "items": [
                {"id": "item_006", "title": "新闻标题F", "content": "这是第六篇新闻的摘要内容。", "created_at": "2023-01-01T10:25:00"},
                {"id": "item_007", "title": "通知公告G", "content": "这是第七篇公告的摘要内容。", "created_at": "2023-01-01T10:30:00"},
                {"id": "item_008", "title": "科技前沿H", "content": "这是第八篇科技文章的摘要内容。", "created_at": "2023-01-01T10:35:00"},
                {"id": "item_009", "title": "生活小贴士I", "content": "这是第九篇生活贴士的摘要内容。", "created_at": "2023-01-01T10:40:00"},
                {"id": "item_010", "title": "产品更新J", "content": "这是第十篇产品更新的摘要内容。", "created_at": "2023-01-01T10:45:00"},
            ],
            "total": 25,
            "page": 2,
            "page_size": 5,
        },
        # 测试用例3: 关键字搜索，第一页，每页10条
        (("keyword", "新闻"), ("page", 1), ("page_size", 10)): {
            "items": [
                {"id": "item_news_01", "title": "突发新闻快报", "content": "今日重要事件的最新报道。", "created_at": "2023-02-01T11:00:00"},
                {"id": "item_news_02", "title": "国际新闻聚焦", "content": "全球热点事件的深度分析。", "created_at": "2023-02-01T11:15:00"},
            ],
            "total": 2, # 假设只搜到2条新闻
            "page": 1,
            "page_size": 10,
        },
        # 测试用例4: 关键字搜索，无结果
        (("keyword", "不存在的关键字"), ("page", 1), ("page_size", 10)): {
            "items": [],
            "total": 0,
            "page": 1,
            "page_size": 10,
        },
        # 测试用例5: 关键字为空字符串，模拟无关键字查询 (Optional[str] 会处理为 None)
        # 如果需要区分 "" 和 None，可以根据业务逻辑调整
        (("keyword", ""), ("page", 1), ("page_size", 10)): {
            "items": [], # 或者返回所有数据的第一页，取决于实际实现
            "total": 0, # 这里假设空字符串关键字不返回任何数据
            "page": 1,
            "page_size": 10,
        },
    }
}
```