#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:02
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : tools.py
import logistics_api_adk_agent.apis
from logistics_api_adk_agent.env import logger


def get_tools():
    # 最终工具集
    _AVAILABLE_FUNCTIONS = {}
    _TOOL_LIST = []

    logger.info("--- 动态生成 API 工具函数 ---")
    for api_meta in logistics_api_adk_agent.apis.apis_list:
        # 调用包装器创建新的函数
        new_func = api_meta.create_api_tool_function()

        # 注册到字典和列表
        _AVAILABLE_FUNCTIONS[new_func.__name__] = new_func
        _TOOL_LIST.append(new_func)

        logger.info(f"  ✅ 生成函数: {new_func.__name__} - {api_meta.describe}")
    logger.info("---")
    return _AVAILABLE_FUNCTIONS, _TOOL_LIST


AVAILABLE_FUNCTIONS, TOOL_LIST = get_tools()
