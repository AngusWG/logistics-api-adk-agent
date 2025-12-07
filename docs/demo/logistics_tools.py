#!/usr/bin/env python
# encoding: utf-8
# @Time   : $DATE.get('yyyy-M-d') 22:57
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : logistics_tools.py
# logistics_tools.py
import json

import requests

# Mock API 服务器的基础 URL
BASE_URL = "http://127.0.0.1:5000/api"


def check_shipping_status(order_id: str):
    """
    通过调用 Mock API，查询特定订单号的最新物流状态。
    Args:
        order_id: 要查询的订单编号。
    Returns:
        包含订单状态信息的JSON字符串。
    """
    try:
        url = f"{BASE_URL}/shipment/status/{order_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 检查 HTTP 错误
        return response.text
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return json.dumps({"error": f"Order ID {order_id} not found."})
        return json.dumps({"error": f"HTTP Error: {e}"})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Network Error: {e}"})


def create_new_shipment(origin: str, destination: str):
    """
    通过调用 Mock API，创建一个新的货运单。
    Args:
        origin: 货物的起始地。
        destination: 货物的目的地。
    Returns:
        包含新货运单号和状态的JSON字符串。
    """
    try:
        url = f"{BASE_URL}/shipment/create"
        payload = {"origin": origin, "destination": destination}
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Network Error or API Down: {e}"})


# ----------------------------------------------------
# 工具 Schema 定义 (用于传递给 Gemini 模型)
# ----------------------------------------------------

# 映射：Python 函数名 -> 实际的 Python 函数对象
AVAILABLE_FUNCTIONS = {
    "check_shipping_status": check_shipping_status,
    "create_new_shipment": create_new_shipment,
}

# 工具列表：将 Python 函数转换为 Gemini 模型可理解的工具列表
TOOL_LIST = [check_shipping_status, create_new_shipment]
