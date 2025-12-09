# todo

## 🎯 ADK 智能体系统开发计划


- [x] logistics_api_adk_agent 项目结构
- [x] 爬取 api 文档
- [x] 丢给 ai 形成 接口
  - 保证通用 使用 pydantic request response 结构
  - 组装成 TOOL_LIST
  - 入口函数 增加 
    - [ ] 交互式
    - [x] 一句话模式
- [ ] 位置日志
- [ ] 测试
- [ ] 错误处理

### 阶段 2：工具定义与 API 模拟（Tooling and Mocking）

- [ ] 分析物流 API 文档 (`http://47.115.60.18/api/doc`)，确定关键功能（例如：查询状态、创建订单）所需的 API 端点和参数。
- [ ] 定义 **工具规范**（函数名称、参数、详细描述），供 ADK 智能体调用。
- [ ] 实现一个模拟的 **物流 API 客户端** 类/模块（例如 `LogisticsApiClient.py`），用于模拟 API 响应和错误情况。
    - [ ] 模拟 `check_shipping_status(order_id)` 函数：返回成功状态（如：“运输中”、“已送达”）和数据。
    - [ ] 模拟 `create_new_shipment(origin, destination, weight, dimensions)` 函数：返回新的货运单号和确认信息。
    - [ ] 模拟边缘情况，如“订单号不存在”或“输入参数无效”时的错误响应。

---

### 阶段 3：ADK 智能体核心实现（ADK Agent Implementation）

- [ ] 设置 Google ADK 环境和所需依赖。
- [x] 定义智能体的系统 **提示/角色**（Prompt/Persona），以确立其物流客服的身份和行为模式。
  - demo 里目前不需要 prompt
- [ ] 将 **模拟物流 API 客户端** 集成并注册为 ADK 智能体的可用工具。
- [ ] 实现智能体主逻辑，使其能够处理用户请求：
    - [x] **意图解析：** 准确识别用户所需的物流操作（查询或创建）。
      - 测试后有问题再弄
    - [ ] **工具选择与执行：** 选取并调用正确的模拟 API 函数。
    - [x] **响应生成：** 将工具返回的模拟数据转换为自然、友好的中文回复。
      - 不用

---

### 阶段 4：测试、错误处理与代码优化（Testing and Refinement）

- [ ] 在模拟客户端和智能体逻辑中实现针对性**错误处理**（例如：模拟网络故障、数据格式错误、必填项缺失）。
- [ ] 测试智能体对核心请求的处理能力：
    - [ ] “Check the shipping status for order \#12345”（查询订单 #12345 的物流状态）
    - [ ] “Create a new shipment from Shenzhen to Los Angeles”（创建一个从深圳到洛杉矶的新货运单）
- [ ] 测试一个边缘案例：“订单 \#999 的状态是什么，这个订单不存在。”
- [ ] 审查和重构代码，确保**代码质量、结构清晰度**和符合生产级标准。

---
