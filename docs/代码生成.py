#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 16:29
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : 代码生成.py
import os
import time

import tqdm
from dotenv import load_dotenv
from google import genai
import lxml.html

load_dotenv("../.env")
prompt = """
参考如下的代码
``` python
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
```

将 ｛page_data｝ 也生成对应的python代码
并生成对应的测试用例
参考
``` python
MOCK_DATA: Dict[Tuple[str, str], Any] = {{
    ("server_status", "get"): {{
        (("keyword", "123456"),): dict(Status="normal", time=mock_time),
        (("keyword", "11222"),): dict(Status="error code", time=mock_time),
        (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    }}
}}
```

请直接给出python代码
测试数据代码用 ### 分割 

"""  # 使用 双大括号 {{ 和 }} 来表示字面量 { 和 }。

client = genai.Client()
code_dir = "genera_code"
os.makedirs(code_dir, exist_ok=True)
file_list = os.listdir("cntodd-apis")[3:]

for index, file in tqdm.tqdm(enumerate(file_list)):
    print(index, file)
    with open(os.path.join("cntodd-apis", file), "r", encoding="utf8") as f:
        html_content = f.read()

    # 节约流量 压缩一下
    xpath = "//div[contains(@class, 'layui-col-sm9')]//text()"
    tree = lxml.html.fromstring(html_content)
    content_data = tree.xpath(xpath)
    format_content = " ".join(content_data)
    format_content = " ".join(format_content.split())
    _prompt = prompt.format(page_data=format_content)
    # print(_prompt)

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    filename = os.path.join(code_dir, file.replace("html", "md"))

    with open(filename, "w", encoding="utf8") as f:
        f.write(response.text.strip())
    print(f"{index} {file} save to {filename}")
    time.sleep(2)
