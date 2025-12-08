#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 0:56
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : __init__.py
from logistics_api_adk_agent.apis.channel import query_channel
from logistics_api_adk_agent.apis.create_fba_order import (
    create_fba_draft,
    create_fba_forecast,
)
from logistics_api_adk_agent.apis.create_order import (
    create_order_draft,
    create_order_forecast,
)
from logistics_api_adk_agent.apis.currency import query_currency
from logistics_api_adk_agent.apis.server_status import server_status

apis_list = [
    server_status,
    query_channel,
    create_fba_draft,
    create_fba_forecast,
    create_order_draft,
    create_order_forecast,
    query_currency,
]
