#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:01
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : agent_client.py


from google.genai import types

from logistics_api_adk_agent.env import genai_client, logger
from logistics_api_adk_agent.tools import AVAILABLE_FUNCTIONS, TOOL_LIST

# 确保设置了 GEMINI_API_KEY 环境变量


def run_agent_workflow(prompt: str) -> str:
    """
    执行智能体工作流程：发送请求 -> 处理函数调用 -> 返回最终回复。
    """
    logger.info(f"用户请求: {prompt}")
    logger.debug("发送请求给 Gemini，进行意图识别 ---")

    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(tools=TOOL_LIST),
    )

    # 2. 检查模型是否决定调用工具
    if not response.function_calls:
        logger.debug("\n--- 2. 模型决定直接回复 (无需工具) ---")
        return response.text

    # 3. 处理函数调用 (执行本地代码)
    logger.debug("\n--- 2. 模型请求调用工具 (执行本地代码) ---")

    # 存储所有函数调用结果，用于第二次调用
    function_responses = []

    for function_call in response.function_calls:
        func_name = function_call.name
        func_args = dict(function_call.args)

        logger.debug(f"   -> 准备调用函数: {func_name}，参数: {func_args}")

        # 查找并执行本地 Python 函数
        if func_name in AVAILABLE_FUNCTIONS:
            # ** 核心步骤：本地执行工具 **
            function_to_call = AVAILABLE_FUNCTIONS[func_name]
            tool_output = function_to_call(**func_args)

            logger.debug(f"   -> 本地工具执行结果: {tool_output}")

            # 准备函数调用的结果对象
            function_responses.append(
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": tool_output},  # 将工具输出作为结果
                )
            )
        else:
            logger.debug(f"错误: 找不到本地工具 {func_name}")

    # 4. 第二次调用：将工具结果回传给模型，生成最终回复
    logger.debug("\n--- 3. 将工具执行结果回传给 Gemini，生成最终回复 ---")

    # 将原始用户请求和第一次模型的响应一起作为上下文
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(prompt)]),
        response.candidates[0].content,
        types.Content(role="tool", parts=function_responses),
    ]

    final_response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(tools=TOOL_LIST),
    )

    return final_response.text
