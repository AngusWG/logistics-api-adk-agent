#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 16:29
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : 代码生成.py
import os
import time

import lxml.html
import retry
import tqdm
from dotenv import load_dotenv
from google import genai

load_dotenv("../.env")
prompt = """
参考如下的代码
``` python
from pydantic import BaseModel, Field

from logistics_api_adk_agent.apis.base import APIInfo

import json
from dataclasses import dataclass
from typing import Callable, Literal, Type

import requests
from pydantic import BaseModel


@dataclass(frozen=True)
class APIInfo:
    name: str
    describe: str
    url: str
    method: Literal["GET", "POST"]
    request_model: Type[BaseModel]
    response_model: Type[BaseModel]

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

将 
｛page_data｝ 
生成对应的python代码
并生成对应的测试用例数据
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

- 请直接给 出python 代码
- 测试用例数据代码用和 ### 分割
- 请只给出 新生成的代码
- 不用给出 APIInfo 定义

"""  # 使用 双大括号 {{ 和 }} 来表示字面量 { 和 }。

client = genai.Client()
code_dir = "genera_code"
os.makedirs(code_dir, exist_ok=True)
file_list = os.listdir("cntodd-apis")


@retry.retry(exceptions=(genai.errors.ClientError), tries=3, delay=5)
def handle_one(file: str, index: int):
    if file.replace("html", "md") in os.listdir(code_dir):
        print(f"已存在 {file} 跳过")
        return

    with open(os.path.join("cntodd-apis", file), "r", encoding="utf8") as f:
        html_content = f.read()

    # 节约流量 压缩一下
    xpath = "//div[contains(@class, 'layui-col-sm9')]//text()"
    tree = lxml.html.fromstring(html_content)
    content_data = tree.xpath(xpath)
    format_content = " ".join(content_data)
    format_content = " ".join(format_content.split())
    _prompt = prompt.replace("｛page_data｝", format_content)
    print(_prompt)
    input("x")
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    target_filename = os.path.join(code_dir, file.replace("html", "md"))
    with open(target_filename, "w", encoding="utf8") as f:
        f.write(response.text.strip())
    print(f"{index} {file} save to {target_filename}")


def main():
    for index, file in enumerate(file_list):
        print(index, file)
        handle_one(file, index)


if __name__ == "__main__":
    main()
