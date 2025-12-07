#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 1:02
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : env.py

import logging
from typing import Optional

import sentry_sdk
from google import genai

from logistics_api_adk_agent.config import conf


def init_sentry(dns: Optional[str]) -> None:
    """初始化 Sentry 监控。"""
    if dns:
        sentry_sdk.init(dsn=dns, traces_sample_rate=1.0)
        logging.getLogger(conf.base.PROJECT_NAME).info("Sentry initialized.")


def init_logging(log_level: str, log_format: str, project_name: str) -> None:
    """
    配置 Python 日志系统的格式和级别。
    """
    base_handler = logging.StreamHandler()

    # 注意：%(name)s 用于区分不同的 logger
    # 假设 conf.LOG_FORMAT 已经包含 %(name)s
    logging.basicConfig(handlers=[base_handler], format=log_format, level=log_level)

    # 设置根 logger 的级别
    root_logger = logging.getLogger()
    try:
        root_logger.setLevel(log_level.upper())
    except ValueError:
        root_logger.setLevel(logging.INFO)  # 默认值

    logging.getLogger(project_name).info("Logger configuration finished.")


# 在模块加载时执行初始化
init_sentry(conf.base.SENTRY_DNS)
init_logging(conf.base.LOG_LEVEL, conf.base.LOG_FORMAT, conf.base.PROJECT_NAME)

# ------------------------------------------------
# 暴露全局 Logger
# ------------------------------------------------
# 按照您的要求，使用配置中的项目名称获取全局 logger 实例。
logger = logging.getLogger(conf.base.PROJECT_NAME)

try:
    genai_client = genai.Client()
except Exception as e:
    logger.error("错误: 无法初始化 Gemini Client。请检查是否设置了 GEMINI_API_KEY 环境变量。")
    logger.error(f"{e}")
    exit()
