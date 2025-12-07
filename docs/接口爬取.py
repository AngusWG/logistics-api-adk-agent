#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 0:26
# @author : zza
# @Email : z740713651@outlook.com
# @File : 接口爬取.py
import os.path

import requests
import tqdm

url = "http://47.115.60.18/api/doc?api=createOrder"
apis = {
    "createOrder": "批量下单 Create Order",
    "createFbaOrder": "Fba批量下单 Create Fba Order",
    "label": "获取标签 Label",
    "Express": "获取面单 Express",
    "delete": "删除运单 delete",
    "waybillnumber": "获取单号 Waybillnumber",
    "pageOrders": "分页查询运单 pageOrders",
    "orderAnnexs": "获取运单附件 orderAnnexs",
    "orderRecSheets": "获取运单费用 orderRecSheets",
    "searchChannelPrice": "运费试算 searchChannelPrice",
    "orderAmt": "获取运单预扣金额 orderAmt",
    "orderVolume": "获取运单收货材积信息 orderVolume",
    "orderPickup": "获取运单提货信息 orderPickup",
    "equipReceipt": "设备收货 equipReceipt",
    "uploadBoxPicture": "上传收货图片 uploadBoxPicture",
    "channel": "查询渠道 Channel",
    "insurance": "查询投保类型 Insurance",
    "productType": "查询物品类别 Product Type",
    "declareType": "查询报关类型 Declare Type",
    "customsType": "查询清关方式 Customs Type",
    "destination": "查询目的地 Destination",
    "currency": "查询币别 Currency",
    "termsofsalecode": "查询销售条款 Terms of sale",
    "exportreasoncode": "查询出口原因 Export reason",
    "track": "查询轨迹 Track",
    "price": "查询报价 Price",
    "dataPush": "数据推送 Data Push",
    "receivePlatformData": "接收平台信息 Receive PlatformData",
}

tar_dir = "cntodd-apis"
os.makedirs(tar_dir, exist_ok=True)
for api_name, cn in tqdm.tqdm(apis.items()):
    resp = requests.get(f"http://47.115.60.18/api/doc?api={api_name}")
    filename = os.path.join(tar_dir, f"{api_name} - {cn}.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(resp.text)
