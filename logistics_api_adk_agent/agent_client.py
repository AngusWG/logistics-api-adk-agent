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


def execute_tool_calls(function_calls: list[types.FunctionCall]) -> list[types.Part]:
    """
    复用工具调用逻辑：接收 FunctionCall 列表，执行本地函数，并返回结果 Part 列表。
    """
    function_responses = []

    for function_call in function_calls:
        func_name = function_call.name
        func_args = dict(function_call.args)

        logger.debug(f"    -> 准备调用函数: {func_name}，参数: {func_args}")

        if func_name in AVAILABLE_FUNCTIONS:

            function_to_call = AVAILABLE_FUNCTIONS[func_name]
            try:
                tool_output = function_to_call(**func_args)
            except Exception as e:
                tool_output = f"工具执行错误: {e}"

            logger.debug(f"    -> 本地工具执行结果: {tool_output}")

            function_responses.append(
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": tool_output},
                )
            )
        else:
            logger.debug(f"错误: 找不到本地工具 {func_name}")

            function_responses.append(
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"本地找不到工具: {func_name}"},
                )
            )

    return function_responses


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

    logger.debug("\n--- 2. 模型请求调用工具 (执行本地代码) ---")

    function_responses = execute_tool_calls(response.function_calls)

    logger.debug("\n--- 3. 将工具执行结果回传给 Gemini，生成最终回复 ---")

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


def run_interactive_chat():
    """
    执行交互式聊天智能体工作流程。
    """
    logger.info("初始化 Gemini 聊天会话，并配置工具。")

    # 1. 创建聊天会话，并在创建时配置工具
    chat = genai_client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(tools=TOOL_LIST),
    )

    print("\n" + "=" * 50)
    print("🤖 智能物流客服已上线！(输入 '退出' 结束会话)")
    print("=" * 50 + "\n")

    # 2. 交互式循环
    while True:
        try:
            # 获取用户输入
            prompt = input("👤 您: ").strip()

            if prompt.lower() in ["退出", "exit", "quit"]:
                print("\n👋 感谢使用，会话结束。")
                break

            if not prompt:
                continue

            logger.info(f"用户请求: {prompt}")

            response = chat.send_message(prompt)

            while response.function_calls:
                logger.debug("\n--- 模型请求调用工具 (执行本地代码) ---")
                function_responses = execute_tool_calls(response.function_calls)
                logger.debug("\n--- 将工具执行结果回传给 Gemini ---")
                response = chat.send_message(function_responses)

            # 模型没有 FunctionCall 时，返回最终文本
            print(f"🤖 客服: {response.text}\n")

        except KeyboardInterrupt:
            print("\n👋 感谢使用，会话结束。")
            break
