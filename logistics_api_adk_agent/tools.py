#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:02
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : tools.py
import logistics_api_adk_agent.apis


def get_tools():
    # 最终工具集
    _AVAILABLE_FUNCTIONS = {}
    _TOOL_LIST = []

    print("--- 动态生成 API 工具函数 ---")
    for api_meta in logistics_api_adk_agent.apis.apis_list:
        # 调用包装器创建新的函数
        new_func = api_meta.create_api_tool_function()

        # 注册到字典和列表
        _AVAILABLE_FUNCTIONS[new_func.__name__] = new_func
        _TOOL_LIST.append(new_func)

        print(f"  ✅ 生成函数: {new_func.__name__}")

    # ------------------------------------
    # 验证和使用 (演示如何像 create_new_shipment 一样调用)
    # ------------------------------------
    print("\n--- 验证生成的工具 ---")

    # 1. 访问第一个工具（对应 CreateShipmentAPI）
    shipment_tool = _AVAILABLE_FUNCTIONS["server_status"]

    # 验证函数名称和 Docstring
    print(f"函数名: {shipment_tool.__name__}")
    print("--- Docstring ---")
    print(shipment_tool.__doc__.strip())
    return _AVAILABLE_FUNCTIONS, _TOOL_LIST


AVAILABLE_FUNCTIONS, TOOL_LIST = get_tools()
