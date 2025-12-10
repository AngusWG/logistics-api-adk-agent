# logistics-api-adk-agent

--- 

AxonScale Interview Question: Google AI Agent

## todo

- [x] 基本功能完成
- [ ] 接口补全
  - [x] channel - 查询渠道 Channel.md
  - [x] createFbaOrder - Fba批量下单 Create Fba Order.md
  - [x] createOrder - 批量下单 Create Order.md
  - [x] currency - 查询币别 Currency.md
  - [x] customsType - 查询清关方式 Customs Type.md
  - [ ] dataPush - 数据推送 Data Push.md
  - [ ] declareType - 查询报关类型 Declare Type.md
  - [ ] delete - 删除运单 delete.md
  - [ ] destination - 查询目的地 Destination.md
  - [ ] equipReceipt - 设备收货 equipReceipt.md
  - [ ] exportreasoncode - 查询出口原因 Export reason.md
  - [ ] Express - 获取面单 Express.md
  - [ ] insurance - 查询投保类型 Insurance.md
  - [ ] label - 获取标签 Label.md
  - [ ] orderAmt - 获取运单预扣金额 orderAmt.md
  - [ ] orderAnnexs - 获取运单附件 orderAnnexs.md
  - [ ] orderPickup - 获取运单提货信息 orderPickup.md
  - [ ] orderRecSheets - 获取运单费用 orderRecSheets.md
  - [ ] orderVolume - 获取运单收货材积信息 orderVolume.md
  - ...

## Features

- logistics-api-adk-agent 是一个通过 http://47.115.60.18/api/doc 文档,
- 通过 Google Gemini AI 操作本地代码 调用 requests 下单的一个工具包.

## How to start

- 需要准备
  - Google Gemini AI token
  - 一个能用的 http://47.115.60.18/api/doc 的服务端地址 url (ip:port, 下列配置中的 SERVER_BASE_URL=)
    - 如果没有, 有一个 [echo_fastapi_server.py](tests/echo_fastapi_server.py) 本地启动的服务都安 可以使用.
  - 将配置放到 logistics-api-adk-agent\.env 文件中

```yaml
# 日志输出格式
# logistics_api_adk_agent__LOG_FORMAT
# 如果需要更改日志等级
logistics_api_adk_agent__LOG_LEVEL=DEBUG
# 如果有 Sentry 部署
logistics_api_adk_agent__SENTRY_DNS 
# 
logistics_api_adk_agent__SERVER_BASE_URL="http://127.0.0.1:8000"
GOOGLE_API_KEY='xxxx'
```

- 安装
  - `pip install .`
- 命令行调用
  - `logistics_api_adk_agent run 查看一下服务器状态"` (只有 echo_fastapi_server 启动时能用)
  - 服务器状态正常，时间是2025-12-10T23:55:10.004413
  - `logistics_api_adk_agent run 帮我查一下系统可用的币别 code KJHBA token c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas`
  - 交互式调用
  - `logistics_api_adk_agent run_with_content 帮我查一下系统可用的币别`

- 程序调用

```python
from logistics_api_adk_agent import run_with_content, run

res = run("查看一下服务器状态")
print(res)
run_with_content("FBA批量下单到草稿")
```

---

## 开发须知

* [Black formatter](https://github.com/psf/black)

> This project use black, please set `Continuation indent` = 4  
> Pycharm - File - Settings - Editor - Code Style - Python - Tabs and Indents

* [Flake8 lint](https://github.com/PyCQA/flake8)

> Use flake8 to check your code style.

* This project is made by [AngusWG/cookiecutter-py-package](https://github.com/AngusWG/cookiecutter-py-package.git)

### debug

- 开发需要安装相关的包 pip install -r requirements_dev.txt
- 建议看一下 docs

- 开发简介
  - 爬取 http://47.115.60.18/api/doc 的接口
  - 将每个接口转换成 一个 RequestModel 和 ResponseModel
    - 通过AI批量转换的
  - 组装成一个 APIInfo
    - name
    - describe
    - url
    - method
    - request_model
    - response_model
  - 然后放到 AI Agent 里, 粗浅的让ai判断要不要调用
    - ai 在调用时产生一个回调
    - 回调完成后再发给ai做参考 回复给用户
