#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 18:32
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : create_order.py
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, confloat, conint, conlist

from logistics_api_adk_agent.apis.base import APIInfo

# 请求参数模型


class Authorization(BaseModel):
    code: str = Field(..., description="客户编码", min_length=5, max_length=20)
    token: str = Field(..., description="API授权码", min_length=50, max_length=50)


class Items(BaseModel):
    skucode: Optional[str] = Field(None, description="商品SKU", max_length=50)
    cnname: Optional[str] = Field(None, description="物品中文名", max_length=100)
    enname: Optional[str] = Field(None, description="物品英文名", max_length=100)
    weight: Optional[float] = Field(None, description="净重(KG)")
    mweight: Optional[float] = Field(None, description="毛重(KG)")
    quantity: Optional[int] = Field(None, description="数量")
    quantityunit: Optional[str] = Field(None, description="数量单位", max_length=10)
    price: Optional[float] = Field(None, description="申报单价")
    declarecurrency: Optional[str] = Field(None, description="申报币别", max_length=10)
    hscode: Optional[str] = Field(None, description="海关编码", max_length=50)
    destinationhscode: Optional[str] = Field(
        None, description="目的地海关编码", max_length=50
    )
    norms: Optional[str] = Field(None, description="规格", max_length=50)
    category: Optional[str] = Field(None, description="类别", max_length=50)
    note: Optional[str] = Field(None, description="配货信息", max_length=200)
    usage: Optional[str] = Field(None, description="用途(中文)", max_length=100)
    enusage: Optional[str] = Field(None, description="用途(英文)", max_length=100)
    material: Optional[str] = Field(None, description="材质（中文）", max_length=100)
    enmaterial: Optional[str] = Field(None, description="材质(英文)", max_length=100)
    salesllink: Optional[str] = Field(None, description="销售链接", max_length=200)
    origin: Optional[str] = Field(None, description="产地", max_length=20)
    brand: Optional[str] = Field(None, description="品牌", max_length=50)
    model: Optional[str] = Field(None, description="型号", max_length=50)
    image: Optional[str] = Field(None, description="产品图片(Base64)")
    imgext: Optional[str] = Field(
        None, description="产品图片格式（.gif、.jpg、.png、.jpeg）"
    )
    isbatterys: int = Field(..., description="是否带电(0：否，1：是)")
    ismagnets: int = Field(..., description="是否带磁(0：否，1：是)")
    isliquids: int = Field(..., description="是否液体(0：否，1：是)")
    ispowders: int = Field(..., description="是否粉末(0：否，1：是)")
    priceexport: Optional[float] = Field(None, description="出口国申报单价")


class Volumes(BaseModel):
    customerchildnumber: Optional[str] = Field(
        None, description="客户子单号", max_length=50
    )
    prenum: Optional[int] = Field(None, description="件数")
    prelength: Optional[float] = Field(None, description="长(CM)")
    prewidth: Optional[float] = Field(None, description="宽(CM)")
    preheight: Optional[float] = Field(None, description="高(CM)")
    prerweight: Optional[float] = Field(None, description="单件重量(KG)")
    palletnum: Optional[int] = Field(None, description="托盘件数")


class Order(BaseModel):
    channelid: str = Field(..., description="收货渠道", max_length=20)
    customernumber1: str = Field(..., description="客户参考号1", max_length=50)
    customernumber2: Optional[str] = Field(
        None, description="客户参考号2", max_length=50
    )
    fbanumber: Optional[str] = Field(None, description="FBA ID", max_length=50)
    number: int = Field(..., description="总件数")
    forecastweight: float = Field(..., description="预报总重量(KG)")
    forecastsquare: Optional[float] = Field(None, description="预报方数")
    isbattery: int = Field(..., description="是否带电(0：否，1：是)")
    ismagnet: Optional[int] = Field(None, description="是否带磁(0：否，1：是)")
    isliquid: Optional[int] = Field(None, description="是否液体(0：否，1：是)")
    ispowder: Optional[int] = Field(None, description="是否粉末(0：否，1：是)")
    packagetypecode: Optional[str] = Field(
        None,
        description="包裹类型 [ G：礼品，C：商品货样，D：文件，O：其它 ]",
        max_length=1,
    )
    goodstypecode: Optional[str] = Field(
        None, description="货物类型 [ WPX：包裹，DOC：文件，PAK：PAK袋 ]", max_length=3
    )
    isinsurance: Optional[int] = Field(None, description="是否投保(0：否，1：是)")
    insurancevalue: Optional[float] = Field(None, description="投保金额, 投保则必需")
    insurancetypepkid: Optional[int] = Field(None, description="投保类型, 投保则必需")
    insurancecurrency: Optional[str] = Field(None, description="投保币别, 投保则必需")
    declaretypepkid: Optional[int] = Field(None, description="报关类型")
    customstype: Optional[str] = Field(None, description="清关方式")
    termsofsalecode: Optional[str] = Field(None, description="销售条款", max_length=3)
    exportreasoncode: Optional[str] = Field(None, description="出口原因", max_length=20)
    producttypepkid: Optional[str] = Field(None, description="物品类别", max_length=20)
    feepaytype: Optional[str] = Field(
        None,
        description="运费支付方式 [ CC：到付，PP：预付，TP：第三方 ]",
        max_length=2,
    )
    feepayname: Optional[str] = Field(
        None, description="运费支付公司或名称", max_length=100
    )
    feepayaccountnumber: Optional[str] = Field(
        None, description="运费支付账号", max_length=50
    )
    feepaycountrycode: Optional[str] = Field(
        None, description="运费支付账号对应国家", max_length=5
    )
    feepaypostcode: Optional[str] = Field(
        None, description="运费支付账号对应邮编", max_length=20
    )
    taxpaytype: Optional[str] = Field(
        None,
        description="税金支付方式 [ CC：到付，PP：预付，TP：第三方 ]",
        max_length=2,
    )
    taxpayname: Optional[str] = Field(
        None, description="税金支付公司或名称", max_length=100
    )
    taxpayaccountnumber: Optional[str] = Field(
        None, description="税金支付账号", max_length=50
    )
    taxpaycountrycode: Optional[str] = Field(
        None, description="税金支付账号对应国家", max_length=5
    )
    taxpayzipcode: Optional[str] = Field(
        None, description="税金支付账号对应邮编", max_length=20
    )
    note: Optional[str] = Field(None, description="运单备注", max_length=255)
    othernote: Optional[str] = Field(None, description="其他备注", max_length=255)
    countrycode: str = Field(..., description="收件人国家编码", max_length=2)
    fbawarehousecode: Optional[str] = Field(None, description="FBA仓码", max_length=20)
    consigneeaddresstype: Optional[str] = Field(
        None, description="收件人地址类型", max_length=20
    )
    consigneename: str = Field(..., description="收件人名称", max_length=100)
    consigneecorpname: Optional[str] = Field(
        None, description="收件人公司", max_length=100
    )
    consigneeaddress1: str = Field(..., description="收件人地址1", max_length=100)
    consigneeaddress2: Optional[str] = Field(
        None, description="收件人地址2", max_length=100
    )
    consigneeaddress3: Optional[str] = Field(
        None, description="收件人地址3", max_length=100
    )
    consigneecity: str = Field(..., description="收件人城市", max_length=50)
    consigneezipcode: str = Field(..., description="收件人邮编", max_length=10)
    consigneeprovince: str = Field(..., description="收件人省州", max_length=50)
    consigneearea: Optional[str] = Field(None, description="收件人区", max_length=50)
    consigneetel: Optional[str] = Field(None, description="收件人电话", max_length=50)
    consigneemobile: Optional[str] = Field(
        None, description="收件人手机", max_length=50
    )
    consigneehousenumber: Optional[str] = Field(
        None, description="收件人门牌号", max_length=20
    )
    consigneetaxnumber: Optional[str] = Field(
        None, description="收件人税号", max_length=50
    )
    consigneeemail: Optional[str] = Field(None, description="收件人邮箱", max_length=50)
    senderaddresstype: Optional[str] = Field(
        None, description="寄件人地址类型", max_length=20
    )
    sendercountrycode: Optional[str] = Field(
        None, description="寄件人国家编码", max_length=2
    )
    sendername: Optional[str] = Field(None, description="寄件人名称", max_length=100)
    sendercorpname: Optional[str] = Field(
        None, description="寄件人公司", max_length=100
    )
    senderaddress1: Optional[str] = Field(
        None, description="寄件人地址1", max_length=100
    )
    senderaddress2: Optional[str] = Field(
        None, description="寄件人地址2", max_length=100
    )
    senderaddress3: Optional[str] = Field(
        None, description="寄件人地址3", max_length=100
    )
    sendercity: Optional[str] = Field(None, description="寄件人城市", max_length=50)
    senderzipcode: Optional[str] = Field(None, description="寄件人邮编", max_length=10)
    senderprovince: Optional[str] = Field(None, description="寄件人省州", max_length=50)
    senderarea: Optional[str] = Field(None, description="寄件人区", max_length=50)
    sendertel: Optional[str] = Field(None, description="寄件人电话", max_length=50)
    sendermobile: Optional[str] = Field(None, description="寄件人手机", max_length=50)
    sendetaxnumber: Optional[str] = Field(None, description="寄件人税号", max_length=50)
    senderemail: Optional[str] = Field(None, description="寄件人邮箱", max_length=50)
    notifyname: Optional[str] = Field(
        None, description="另通知人/进口商名称", max_length=100
    )
    notifycorpname: Optional[str] = Field(
        None, description="另通知人/进口商公司", max_length=100
    )
    notifycountrycode: Optional[str] = Field(
        None, description="另通知人/进口商国家", max_length=5
    )
    notifyaddress1: Optional[str] = Field(
        None, description="另通知人/进口商地址1", max_length=100
    )
    notifyaddress2: Optional[str] = Field(
        None, description="另通知人/进口商地址2", max_length=100
    )
    notifyaddress3: Optional[str] = Field(
        None, description="另通知人/进口商地址3", max_length=100
    )
    notifycity: Optional[str] = Field(
        None, description="另通知人/进口商城市", max_length=100
    )
    notifyzipcode: Optional[str] = Field(
        None, description="另通知人/进口商邮编", max_length=20
    )
    notifyprovince: Optional[str] = Field(
        None, description="另通知人/进口商省州", max_length=100
    )
    notifytel: Optional[str] = Field(
        None, description="另通知人/进口商电话", max_length=50
    )
    notifymoble: Optional[str] = Field(
        None, description="另通知人/进口商手机", max_length=50
    )
    notifyfax: Optional[str] = Field(
        None, description="另通知人/进口商传真", max_length=50
    )
    notifytaxnumber: Optional[str] = Field(
        None, description="另通知人/进口商税号", max_length=50
    )
    notifyemail: Optional[str] = Field(
        None, description="另通知人/进口商邮箱", max_length=50
    )
    vatnumber: Optional[str] = Field(None, description="VAT/税号", max_length=50)
    eorinumber: Optional[str] = Field(None, description="EORI/企业号", max_length=50)
    vatcorpname: Optional[str] = Field(None, description="VAT公司名称", max_length=100)
    vataddress: Optional[str] = Field(None, description="VAT公司地址", max_length=200)
    freight: Optional[float] = Field(None, description="打单运费")
    extrafees: Optional[float] = Field(None, description="打单杂费")
    currencycode: Optional[str] = Field(None, description="费用币别", max_length=5)
    residential: Optional[str] = Field(
        None, description="是否住宅地址（0：否，1：是）", max_length=1
    )
    ispaperless: Optional[int] = Field(None, description="是否无纸化（2：是）")
    deliverysitecode: Optional[str] = Field(None, description="预计交货站点")
    deliverydate: Optional[str] = Field(None, description="预计交货时间")
    resdelivertime: Optional[str] = Field(
        None, description="亚马逊预计送达时段(如：2025-09-30)"
    )
    interfacefieldvalue: Optional[str] = Field(
        None, description="其它扩展字段, JSON字符串格式"
    )
    platformbillid: Optional[str] = Field(None, description="尾程单号", max_length=50)
    labeldata: Optional[str] = Field(None, description="平台标签 使用完整的URL传值")
    ecplatform: Optional[str] = Field(None, description="电商平台")
    prodsalesname: Optional[str] = Field(None, description="生产销售企业单位")
    prodsalescode: Optional[str] = Field(None, description="生产销售企业代码")


class Data(BaseModel):
    order: Order = Field(..., description="每个运单数据")
    volumes: Optional[List[Volumes]] = Field(None, description="材积信息")
    items: Optional[List[Items]] = Field(None, description="物品信息")


class CreateOrderRequest(BaseModel):
    authorization: Authorization = Field(..., description="接口效验信息")
    datas: List[Data] = Field(..., description="本次提交数据集")


# 响应数据模型


class Child(BaseModel):
    customernumber: str = Field(..., description="客户子单号")
    systemnumber: str = Field(..., description="系统子单号")
    tracknumber: Optional[str] = Field(None, description="转单子单号")


class ResponseData(BaseModel):
    code: int = Field(..., description="下单是否成功 0：表示接口请求通过，-1：表示失败")
    msg: str = Field(..., description="说明信息")
    customernumber: Optional[str] = Field(None, description="客户参考号1")
    systemnumber: Optional[str] = Field(None, description="我方系统单号")
    waybillnumber: Optional[str] = Field(None, description="运单号")
    shortnumber: Optional[str] = Field(None, description="短单号")
    isRemote: Optional[bool] = Field(None, description="是否偏远")
    childs: Optional[List[Child]] = Field(None, description="子单号列表")


class CreateOrderResponse(BaseModel):
    """
    >>> from logistics_api_adk_agent import run
    >>> # 场景 1: 批量下单到草稿 - 成功案例 (使用 create_order_draft)
    >>> # 模拟用户的自然语言请求，包含授权信息和下单意图
    >>> prompt_success = "我需要创建一批运单到草稿，客户编码是 KJHBA，授权码是 60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas，货物信息是 5 件货，总重 77.75KG，渠道 HK_TNT，收件地址是俄罗斯 RU，收件人 Nwabisa Mkaka，邮编 13958，详情：有 5 个包裹，长宽高都为 50CM，单件重 15.55KG，内含 10 个手机壳，单价 5.87 USD，不带电、磁、液、粉"
    >>> res_success = run(prompt_success)
    >>> assert "调用成功" in res_success
    >>> assert "下单成功" in res_success
    >>> assert "T620200611-1001" in res_success # 检查客户参考号
    >>> assert "EV2145664012CN" in res_success # 检查是否返回运单号
    >>> assert "子单号" in res_success # 检查是否返回子单号信息
    >>> assert "是否偏远" in res_success # 检查是否返回 isRemote 字段
    >>> # 场景 2: 授权失败案例 (code=1001)
    >>> prompt_auth_fail = "我需要创建运单到草稿箱，客户编码 ERROR，授权码 invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx，我有一件货，总重 1KG，渠道 HK_TNT，收件人 Test，地址在中国 CN"
    >>> res_auth_fail = run(prompt_auth_fail)
    >>> assert "授权失败" in res_auth_fail
    >>> assert "1001" in res_auth_fail
    >>> # 场景 3: 业务数据校验失败案例 (返回 code=0, data.code=-1)
    >>> # 模拟请求中缺失了必填的 customernumber1 字段
    >>> prompt_data_fail = "我要创建运单到草稿箱，客户编码 KJHBA，授权码 60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas，货物信息是 5 件货，渠道 HK_TNT，收件地址是俄罗斯 RU，但这次没有提供客户参考号"
    >>> res_data_fail = run(prompt_data_fail)
    >>> assert "运单客户参考号1" in res_data_fail
    >>> assert "-1" in res_data_fail
    """

    code: int = Field(
        ..., description="接口请求是否通过 0：表示接口请求通过，其他表示失败"
    )
    msg: str = Field(..., description="说明信息")
    data: List[ResponseData] = Field(..., description="下单结果数据集")


# APIInfo 实例 (两个接口地址)
create_order_draft = APIInfo(
    name="create_order_draft",
    describe="批量下单到草稿",
    url="/api/order/create",
    method="POST",
    request_model=CreateOrderRequest,
    response_model=CreateOrderResponse,
)

create_order_forecast = APIInfo(
    name="create_order_forecast",
    describe="批量下单到预报",
    url="/api/order/createForecast",
    method="POST",
    request_model=CreateOrderRequest,
    response_model=CreateOrderResponse,
)
