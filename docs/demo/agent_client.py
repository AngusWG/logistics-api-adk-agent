#!/usr/bin/env python
# encoding: utf-8
# @Time   : $DATE.get('yyyy-M-d') 22:57
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : agent_client.py
# agent_client.py
from google import genai
from google.genai import types
from logistics_tools import TOOL_LIST, AVAILABLE_FUNCTIONS
import json
import os

# 确保设置了 GEMINI_API_KEY 环境变量
try:
    client = genai.Client()
except Exception as e:
    print("错误: 无法初始化 Gemini Client。请检查是否设置了 GEMINI_API_KEY 环境变量。")
    exit()


def run_agent_workflow(prompt: str):
    """
    执行智能体工作流程：发送请求 -> 处理函数调用 -> 返回最终回复。
    """
    print(f"\n用户请求: {prompt}")

    # 1. 第一次调用：发送用户请求和工具列表
    print("\n--- 1. 发送请求给 Gemini，进行意图识别 ---")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(tools=TOOL_LIST)
    )

    # 2. 检查模型是否决定调用工具
    if not response.function_calls:
        print("\n--- 2. 模型决定直接回复 (无需工具) ---")
        return response.text

    # 3. 处理函数调用 (执行本地代码)
    print("\n--- 2. 模型请求调用工具 (执行本地代码) ---")

    # 存储所有函数调用结果，用于第二次调用
    function_responses = []

    for function_call in response.function_calls:
        func_name = function_call.name
        func_args = dict(function_call.args)

        print(f"   -> 准备调用函数: {func_name}，参数: {func_args}")

        # 查找并执行本地 Python 函数
        if func_name in AVAILABLE_FUNCTIONS:
            # ** 核心步骤：本地执行工具 **
            function_to_call = AVAILABLE_FUNCTIONS[func_name]
            tool_output = function_to_call(**func_args)

            print(f"   -> 本地工具执行结果: {tool_output}")

            # 准备函数调用的结果对象
            function_responses.append(
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": tool_output}  # 将工具输出作为结果
                )
            )
        else:
            print(f"错误: 找不到本地工具 {func_name}")

    # 4. 第二次调用：将工具结果回传给模型，生成最终回复
    print("\n--- 3. 将工具执行结果回传给 Gemini，生成最终回复 ---")

    # 将原始用户请求和第一次模型的响应一起作为上下文
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(prompt)]),
        response.candidates[0].content,
        types.Content(role="tool", parts=function_responses)
    ]

    final_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(tools=TOOL_LIST)
    )

    return final_response.text


# ----------------------------------------------------
# 运行示例
# ----------------------------------------------------

if __name__ == '__main__':
    # 确保 app.py 服务端已在另一个终端启动！

    # 案例 1: 查询状态
    query_status = "请查询订单号 12345 的最新物流状态。"
    final_answer_1 = run_agent_workflow(query_status)
    print("\n=============================================")
    print(f"✅ 最终回复 (查询): {final_answer_1}")
    print("=============================================")

    # 案例 2: 创建货运单
    query_create = "我想创建一个从深圳到洛杉矶的货运单。"
    final_answer_2 = run_agent_workflow(query_create)
    print("\n=============================================")
    print(f"✅ 最终回复 (创建): {final_answer_2}")
    print("=============================================")

    # 案例 3: 边缘情况 (未找到)
    query_not_found = "订单号 99999 的状态是什么？"
    final_answer_3 = run_agent_workflow(query_not_found)
    print("\n=============================================")
    print(f"✅ 最终回复 (未找到): {final_answer_3}")
    print("=============================================")