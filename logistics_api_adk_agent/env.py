#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:02
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : env.py

import logging
import os
from typing import Optional

import sentry_sdk
from google import genai

from logistics_api_adk_agent.config import conf


def init_sentry(dns: Optional[str]) -> None:
    """初始化 Sentry 监控。"""
    if dns:
        sentry_sdk.init(dsn=dns, traces_sample_rate=1.0)
        logging.getLogger(conf.base.PROJECT_NAME).info("Sentry initialized.")


def setup_logging():
    # 创建一个控制台处理器
    base_handler = logging.StreamHandler()

    # 构建日志文件的完整路径
    log_file_path = os.path.join(conf.log_file_dir, f"{conf.PROJECT_NAME}.log")

    # 确保日志文件所在目录存在，如果不存在则创建
    if not os.path.exists(conf.log_file_dir):
        os.makedirs(conf.log_file_dir)

    # 创建一个文件处理器，指定日志文件的完整路径
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")

    # 设置日志格式
    formatter = logging.Formatter(conf.LOG_FORMAT)
    base_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 配置日志记录器，添加控制台处理器和文件处理器
    logging.basicConfig(handlers=[base_handler, file_handler], format=conf.LOG_FORMAT)


logger = logging.getLogger(conf.PROJECT_NAME)
setup_logging()
logger.setLevel(conf.LOG_LEVEL)

try:
    genai_client = genai.Client()
except Exception as e:
    logger.error(
        "错误: 无法初始化 Gemini Client。请检查是否设置了 GEMINI_API_KEY 环境变量。"
    )
    logger.error(f"{e}")
    exit()
