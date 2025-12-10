from pydantic import BaseModel, Field, conlist, conint, confloat
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime

# 请求参数模型

class Authorization(BaseModel):
    code: str = Field(..., description="客户编码", min_length=5, max_length=20)
    token: str = Field(..., description="API授权码", min_length=50, max_length=50)

class Items(BaseModel):
    number: str = Field(..., description="箱序号（如第一箱传 1 ，如第 2 到第 10 箱 都装有该物品则传 2-10）", max_length=20)
    skucode: Optional[str] = Field(None, description="商品SKU", max_length=50)
    cnname: str = Field(..., description="物品中文名", max_length=100)
    enname: str = Field(..., description="物品英文名", max_length=100)
    weight: confloat(gt=0) = Field(..., description="单箱物品净重(KG)")
    mweight: Optional[confloat(gt=0)] = Field(None, description="单箱物品毛重(KG)")
    quantity: conint(ge=1) = Field(..., description="单箱数量")
    quantityunit: Optional[str] = Field(None, description="数量单位", max_length=10)
    price: confloat(ge=0) = Field(..., description="申报单价")
    declarecurrency: str = Field(..., description="申报币别", max_length=10)
    hscode: Optional[str] = Field(None, description="海关编码", max_length=50)
    destinationhscode: Optional[str] = Field(None, description="目的地海关编码", max_length=50)
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
    boxnumber: Optional[str] = Field(None, description="物品箱号", max_length=50)
    fbanumber: Optional[str] = Field(None, description="物品FBA ID", max_length=50)
    poanumber: Optional[str] = Field(None, description="物品POAnimber", max_length=50)
    image: Optional[str] = Field(None, description="产品图片(Base64)")
    imgext: Optional[str] = Field(None, description="产品图片格式（.gif、.jpg、.png、.jpeg）")
    isbatterys: conint(ge=0, le=1) = Field(..., description="是否带电(0：否，1：是)")
    ismagnets: conint(ge=0, le=1) = Field(..., description="是否带磁(0：否，1：是)")
    isliquids: conint(ge=0, le=1) = Field(..., description="是否液体(0：否，1：是)")
    ispowders: conint(ge=0, le=1) = Field(..., description="是否粉末(0：否，1：是)")

class Volumes(BaseModel):
    number: str = Field(..., description="箱序号（如第一箱传 1 ，如第 2 到第 5 箱 长，宽，高 相同时 传 2-5，箱序号 不可重复）", max_length=20)
    customerchildnumber: Optional[str] = Field(None, description="客户子单号", max_length=50)
    prelength: confloat(gt=0) = Field(..., description="长(CM)")
    prewidth: confloat(gt=0) = Field(..., description="宽(CM)")
    preheight: confloat(gt=0) = Field(..., description="高(CM)")
    prerweight: confloat(gt=0) = Field(..., description="单件重量(KG)")
    palletnum: Optional[conint(ge=0)] = Field(None, description="托盘件数")

class Order(BaseModel):
    channelid: str = Field(..., description="收货渠道", max_length=20)
    customernumber1: str = Field(..., description="客户参考号1", max_length=50)
    customernumber2: Optional[str] = Field(None, description="客户参考号2", max_length=50)
    fbanumber: Optional[str] = Field(None, description="FBA ID", max_length=50)
    poanumber: Optional[str] = Field(None, description="POANumber", max_length=50)
    number: conint(ge=1) = Field(..., description="总件数")
    forecastweight: confloat(gt=0) = Field(..., description="预报总重量(KG)")
    forecastsquare: Optional[confloat(ge=0)] = Field(None, description="预报方数")
    isbattery: conint(ge=0, le=1) = Field(..., description="是否带电(0：否，1：是)")
    ismagnet: Optional[conint(ge=0, le=1)] = Field(None, description="是否带磁(0：否，1：是)")
    isliquid: Optional[conint(ge=0, le=1)] = Field(None, description="是否液体(0：否，1：是)")
    ispowder: Optional[conint(ge=0, le=1)] = Field(None, description="是否粉末(0：否，1：是)")
    packagetypecode: Optional[str] = Field(None, description="包裹类型 [ G：礼品，C：商品货样，D：文件，O：其它 ]", max_length=1)
    goodstypecode: Optional[str] = Field(None, description="货物类型 [ WPX：包裹，DOC：文件，PAK：PAK袋 ]", max_length=3)
    isinsurance: Optional[conint(ge=0, le=1)] = Field(None, description="是否投保(0：否，1：是)")
    insurancevalue: Optional[confloat(ge=0)] = Field(None, description="投保金额, 投保则必需")
    insurancetypepkid: Optional[int] = Field(None, description="投保类型, 投保则必需")
    insurancecurrency: Optional[str] = Field(None, description="投保币别, 投保则必需")
    declaretypepkid: Optional[int] = Field(None, description="报关类型")
    customstype: Optional[str] = Field(None, description="清关方式")
    termsofsalecode: Optional[str] = Field(None, description="销售条款", max_length=3)
    exportreasoncode: Optional[str] = Field(None, description="出口原因", max_length=20)
    producttypepkid: Optional[str] = Field(None, description="物品类别", max_length=20)
    feepaytype: Optional[str] = Field(None, description="运费支付方式 [ CC：到付，PP：预付，TP：第三方 ]", max_length=2)
    feepayname: Optional[str] = Field(None, description="运费支付公司或名称", max_length=100)
    feepayaccountnumber: Optional[str] = Field(None, description="运费支付账号", max_length=50)
    feepaycountrycode: Optional[str] = Field(None, description="运费支付账号对应国家", max_length=5)
    feepaypostcode: Optional[str] = Field(None, description="运费支付账号对应邮编", max_length=20)
    taxpaytype: Optional[str] = Field(None, description="税金支付方式 [ CC：到付，PP：预付，TP：第三方 ]", max_length=2)
    taxpayname: Optional[str] = Field(None, description="税金支付公司或名称", max_length=100)
    taxpayaccountnumber: Optional[str] = Field(None, description="税金支付账号", max_length=50)
    taxpaycountrycode: Optional[str] = Field(None, description="税金支付账号对应国家", max_length=5)
    taxpayzipcode: Optional[str] = Field(None, description="税金支付账号对应邮编", max_length=20)
    note: Optional[str] = Field(None, description="运单备注", max_length=255)
    othernote: Optional[str] = Field(None, description="其他备注", max_length=255)
    countrycode: str = Field(..., description="收件人国家编码", max_length=2)
    fbawarehousecode: Optional[str] = Field(None, description="FBA仓码", max_length=20)
    consigneeaddresstype: Optional[str] = Field(None, description="收件人地址类型", max_length=20)
    consigneename: str = Field(..., description="收件人名称", max_length=100)
    consigneecorpname: Optional[str] = Field(None, description="收件人公司", max_length=100)
    consigneeaddress1: str = Field(..., description="收件人地址1", max_length=100)
    consigneeaddress2: Optional[str] = Field(None, description="收件人地址2", max_length=100)
    consigneeaddress3: Optional[str] = Field(None, description="收件人地址3", max_length=100)
    consigneecity: str = Field(..., description="收件人城市", max_length=50)
    consigneezipcode: str = Field(..., description="收件人邮编", max_length=10)
    consigneeprovince: str = Field(..., description="收件人省州", max_length=50)
    consigneearea: Optional[str] = Field(None, description="收件人区", max_length=50)
    consigneetel: Optional[str] = Field(None, description="收件人电话", max_length=50)
    consigneemobile: Optional[str] = Field(None, description="收件人手机", max_length=50)
    consigneehousenumber: Optional[str] = Field(None, description="收件人门牌号", max_length=20)
    consigneetaxnumber: Optional[str] = Field(None, description="收件人税号", max_length=50)
    consigneeemail: Optional[str] = Field(None, description="收件人邮箱", max_length=50)
    senderaddresstype: Optional[str] = Field(None, description="寄件人地址类型", max_length=20)
    sendercountrycode: Optional[str] = Field(None, description="寄件人国家编码", max_length=2)
    sendername: Optional[str] = Field(None, description="寄件人名称", max_length=100)
    sendercorpname: Optional[str] = Field(None, description="寄件人公司", max_length=100)
    senderaddress1: Optional[str] = Field(None, description="寄件人地址1", max_length=100)
    senderaddress2: Optional[str] = Field(None, description="寄件人地址2", max_length=100)
    senderaddress3: Optional[str] = Field(None, description="寄件人地址3", max_length=100)
    sendercity: Optional[str] = Field(None, description="寄件人城市", max_length=50)
    senderzipcode: Optional[str] = Field(None, description="寄件人邮编", max_length=10)
    senderprovince: Optional[str] = Field(None, description="寄件人省州", max_length=50)
    senderarea: Optional[str] = Field(None, description="寄件人区", max_length=50)
    sendertel: Optional[str] = Field(None, description="寄件人电话", max_length=50)
    sendermobile: Optional[str] = Field(None, description="寄件人手机", max_length=50)
    sendetaxnumber: Optional[str] = Field(None, description="寄件人税号", max_length=50)
    senderemail: Optional[str] = Field(None, description="寄件人邮箱", max_length=50)
    notifyname: Optional[str] = Field(None, description="另通知人/进口商名称", max_length=100)
    notifycorpname: Optional[str] = Field(None, description="另通知人/进口商公司", max_length=100)
    notifycountrycode: Optional[str] = Field(None, description="另通知人/进口商国家", max_length=5)
    notifyaddress1: Optional[str] = Field(None, description="另通知人/进口商地址1", max_length=100)
    notifyaddress2: Optional[str] = Field(None, description="另通知人/进口商地址2", max_length=100)
    notifyaddress3: Optional[str] = Field(None, description="另通知人/进口商地址3", max_length=100)
    notifycity: Optional[str] = Field(None, description="另通知人/进口商城市", max_length=100)
    notifyzipcode: Optional[str] = Field(None, description="另通知人/进口商邮编", max_length=20)
    notifyprovince: Optional[str] = Field(None, description="另通知人/进口商省州", max_length=100)
    notifytel: Optional[str] = Field(None, description="另通知人/进口商电话", max_length=50)
    notifymoble: Optional[str] = Field(None, description="另通知人/进口商手机", max_length=50)
    notifyfax: Optional[str] = Field(None, description="另通知人/进口商传真", max_length=50)
    notifytaxnumber: Optional[str] = Field(None, description="另通知人/进口商税号", max_length=50)
    notifyemail: Optional[str] = Field(None, description="另通知人/进口商邮箱", max_length=50)
    vatnumber: Optional[str] = Field(None, description="VAT/税号", max_length=50)
    eorinumber: Optional[str] = Field(None, description="EORI/企业号", max_length=50)
    vatcorpname: Optional[str] = Field(None, description="VAT公司名称", max_length=100)
    vataddress: Optional[str] = Field(None, description="VAT公司地址", max_length=200)
    freight: Optional[confloat(ge=0)] = Field(None, description="打单运费")
    extrafees: Optional[confloat(ge=0)] = Field(None, description="打单杂费")
    currencycode: Optional[str] = Field(None, description="费用币别", max_length=5)
    residential: Optional[str] = Field(None, description="是否住宅地址（0：否，1：是）", max_length=1)
    ispaperless: Optional[conint(ge=1, le=2)] = Field(None, description="是否无纸化（2：是）")
    deliverysitecode: Optional[str] = Field(None, description="预计交货站点")
    deliverydate: Optional[str] = Field(None, description="预计交货时间")
    resdelivertime: Optional[str] = Field(None, description="亚马逊预计送达时段(如：2025-09-30)")
    interfacefieldvalue: Optional[str] = Field(None, description="其它扩展字段, JSON字符串格式")
    platformbillid: Optional[str] = Field(None, description="尾程单号", max_length=50)
    labeldata: Optional[str] = Field(None, description="平台标签 使用完整的URL传值")

class Data(BaseModel):
    order: Order = Field(..., description="每个运单数据")
    volumes: conlist(Volumes, min_length=1) = Field(..., description="材积信息")
    items: conlist(Items, min_length=1) = Field(..., description="物品信息")

class CreateFbaOrderRequest(BaseModel):
    authorization: Authorization = Field(..., description="接口效验信息")
    datas: conlist(Data, min_length=1) = Field(..., description="本次提交数据集")

# 响应数据模型

class Child(BaseModel):
    customernumber: str = Field(..., description="客户子单号")
    systemnumber: str = Field(..., description="系统子单号")
    tracknumber: str = Field(..., description="转单子单号")

class ResponseData(BaseModel):
    code: conint(ge=-1, le=0) = Field(..., description="下单是否成功 0：表示接口请求通过，-1：表示失败")
    msg: str = Field(..., description="说明信息")
    customernumber: Optional[str] = Field(None, description="客户参考号1")
    systemnumber: Optional[str] = Field(None, description="我方系统单号")
    waybillnumber: Optional[str] = Field(None, description="运单号")
    childs: Optional[List[Child]] = Field(None, description="子单号列表")

class CreateFbaOrderResponse(BaseModel):
    code: conint(ge=0) = Field(..., description="接口请求是否通过 0：表示接口请求通过，其他表示失败")
    msg: str = Field(..., description="说明信息")
    data: List[ResponseData] = Field(..., description="下单结果数据集")

# APIInfo 实例 (两个接口地址)
create_fba_draft = APIInfo(
    name="create_fba_draft",
    describe="FBA批量下单到草稿",
    url="http://www.cntodd.top//api/order/createFba",
    method="POST",
    request_model=CreateFbaOrderRequest,
    response_model=CreateFbaOrderResponse,
)

create_fba_forecast = APIInfo(
    name="create_fba_forecast",
    describe="FBA批量下单到预报",
    url="http://www.cntodd.top//api/order/createFbaForecast",
    method="POST",
    request_model=CreateFbaOrderRequest,
    response_model=CreateFbaOrderResponse,
)

###

mock_time = datetime.now().isoformat()

# 示例请求数据
mock_request_data_success = {
    "authorization": {
        "code": "KJHBA",
        "token": "60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"
    },
    "datas": [
        {
            "order": {
                "channelid": "HK_TNT",
                "customernumber1": "T620200611-1001",
                "customernumber2": "",
                "number": 5,
                "isbattery": 0,
                "isinsurance": 0,
                "forecastweight": 77.75, # 15.55 * 5
                "packagetypecode": "O",
                "goodstypecode": "WPX",
                "countrycode": "RU",
                "consigneename": "Nwabisa Mkaka",
                "consigneecorpname": "Nwabisa Mkaka",
                "consigneeaddress1": "nah Iskan 2 Khamis",
                "consigneeaddress2": "Mushait 62444-8888",
                "consigneeaddress3": "",
                "consigneecity": "Khamis Mushait",
                "consigneezipcode": "13958",
                "consigneeprovince": "Asir",
                "consigneetel": "546102083",
                "consigneemobile": "546102083",
                "consigneehousenumber": "A306",
                "consigneetaxnumber": "A068-02",
                "consigneeemail": "admin@Nwabisa.com",
                "deliverysitecode": "0527",
                "isbattery": 0,
            },
            "volumes": [
                {
                    "number": "1",
                    "customerchildnumber": "CH-85120-1001",
                    "prewidth": 50.0,
                    "prelength": 50.0,
                    "preheight": 50.0,
                    "prerweight": 15.55
                },
                {
                    "number": "2-5",
                    "customerchildnumber": "CH-85120-1002",
                    "prewidth": 50.0,
                    "prelength": 50.0,
                    "preheight": 50.0,
                    "prerweight": 15.55
                }
            ],
            "items": [
                {
                    "number": "1-5",
                    "skucode": "PK-08-001",
                    "cnname": "手机壳",
                    "enname": "iphone case",
                    "hscode": "PK896732",
                    "quantity": 10,
                    "quantityunit": "PCS",
                    "price": 5.87,
                    "declarecurrency": "USD",
                    "weight": 1.15,
                    "origin": "CN",
                    "model": "P40",
                    "note": "华为 P40 手机壳",
                    "material": "ABS",
                    "brand": "华为",
                    "usage": "手机保护",
                    "isbatterys": 0,
                    "ismagnets": 0,
                    "isliquids": 0,
                    "ispowders": 0,
                }
            ]
        }
    ]
}

# 示例响应数据
mock_response_data_success = {
    "code": 0,
    "msg": "调用成功",
    "data": [
        {
            "code": 0,
            "msg": "下单成功",
            "customernumber": "T620200611-1001",
            "systemnumber": "1591857709631",
            "waybillnumber": "EV2145664012CN",
            "childs": [
                {"customernumber": "CH-85120-1001", "systemnumber": "1591857709631-1", "tracknumber": "1Z76V3R40448621361"},
                {"customernumber": "CH-85120-1002", "systemnumber": "1591857709631-2", "tracknumber": "1Z76V3R40448621362"},
                {"customernumber": "CH-85120-1003", "systemnumber": "1591857709631-3", "tracknumber": "1Z76V3R40448621363"},
                {"customernumber": "CH-85120-1004", "systemnumber": "1591857709631-4", "tracknumber": "1Z76V3R40448621363"},
                {"customernumber": "CH-85120-1005", "systemnumber": "1591857709631-5", "tracknumber": "1Z76V3R40448621363"},
            ]
        }
    ]
}

mock_request_data_fail_auth = {
    "authorization": {
        "code": "ERROR",
        "token": "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    },
    "datas": [
        # 即使数据正确，授权失败也会导致调用失败
        mock_request_data_success["datas"][0]
    ]
}

mock_response_data_fail_auth = {
    "code": 1001,
    "msg": "授权失败，请检查code和token",
    "data": []
}

mock_request_data_fail_data = {
    "authorization": {
        "code": "KJHBA",
        "token": "60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"
    },
    "datas": [
        {
            "order": {
                # 必填字段缺失: customernumber1
                "channelid": "HK_TNT",
                "number": 5,
                "isbattery": 0,
                "isinsurance": 0,
                "forecastweight": 77.75,
                "packagetypecode": "O",
                "goodstypecode": "WPX",
                "countrycode": "RU",
                "consigneename": "Nwabisa Mkaka",
                "consigneeaddress1": "nah Iskan 2 Khamis",
                "consigneecity": "Khamis Mushait",
                "consigneezipcode": "13958",
                "consigneeprovince": "Asir",
                "isbattery": 0,
            },
            "volumes": [
                {
                    "number": "1",
                    "customerchildnumber": "CH-85120-1001",
                    "prewidth": 50.0,
                    "prelength": 50.0,
                    "preheight": 50.0,
                    "prerweight": 15.55
                }
            ],
            "items": [
                {
                    "number": "1",
                    "cnname": "手机壳",
                    "enname": "iphone case",
                    "quantity": 10,
                    "price": 5.87,
                    "declarecurrency": "USD",
                    "weight": 1.15,
                    "isbatterys": 0,
                    "ismagnets": 0,
                    "isliquids": 0,
                    "ispowders": 0,
                }
            ]
        }
    ]
}

mock_response_data_fail_data = {
    "code": 0,
    "msg": "调用成功",
    "data": [
        {
            "code": -1,
            "msg": "下单失败: 运单客户参考号1 (customernumber1) 为必填项",
            "customernumber": None,
            "systemnumber": None,
            "waybillnumber": None,
            "childs": None,
        }
    ]
}

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("create_fba_draft", "post"): {
        (
            ("authorization", (("code", "KJHBA"), ("token", "60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"))),
            ("datas", (
                (
                    ("order", (("channelid", "HK_TNT"), ("customernumber1", "T620200611-1001"), ("number", 5), ("forecastweight", 77.75), ("isbattery", 0), ("countrycode", "RU"), ("consigneename", "Nwabisa Mkaka"), ("consigneeaddress1", "nah Iskan 2 Khamis"), ("consigneecity", "Khamis Mushait"), ("consigneezipcode", "13958"), ("consigneeprovince", "Asir"))),
                    ("volumes", (("number", "1"), ("prewidth", 50.0), ("prelength", 50.0), ("preheight", 50.0), ("prerweight", 15.55)), (("number", "2-5"), ("prewidth", 50.0), ("prelength", 50.0), ("preheight", 50.0), ("prerweight", 15.55))),
                    ("items", (("number", "1-5"), ("cnname", "手机壳"), ("enname", "iphone case"), ("weight", 1.15), ("quantity", 10), ("price", 5.87), ("declarecurrency", "USD"), ("isbatterys", 0), ("ismagnets", 0), ("isliquids", 0), ("ispowders", 0))),
                ),
            )),
        ): mock_response_data_success,
        (
            ("authorization", (("code", "ERROR"), ("token", "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"))),
            # 简化请求数据，只保留必须字段，以匹配授权失败的用例
            ("datas", (
                (
                    ("order", (("channelid", "HK_TNT"), ("customernumber1", "FAIL_AUTH"), ("number", 1), ("forecastweight", 1.0), ("isbattery", 0), ("countrycode", "CN"), ("consigneename", "Test"), ("consigneeaddress1", "Test Addr"), ("consigneecity", "Test City"), ("consigneezipcode", "100000"), ("consigneeprovince", "Test Prov"))),
                    ("volumes", (("number", "1"), ("prewidth", 10.0), ("prelength", 10.0), ("preheight", 10.0), ("prerweight", 1.0))),
                    ("items", (("number", "1"), ("cnname", "测试品"), ("enname", "Test Item"), ("weight", 0.1), ("quantity", 1), ("price", 1.0), ("declarecurrency", "USD"), ("isbatterys", 0), ("ismagnets", 0), ("isliquids", 0), ("ispowders", 0))),
                ),
            )),
        ): mock_response_data_fail_auth,
        (
            ("authorization", (("code", "KJHBA"), ("token", "60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"))),
            ("datas", (
                (
                    # customernumber1 缺失，模拟数据校验失败
                    ("order", (("channelid", "HK_TNT"), ("number", 5), ("forecastweight", 77.75), ("isbattery", 0), ("countrycode", "RU"), ("consigneename", "Nwabisa Mkaka"), ("consigneeaddress1", "nah Iskan 2 Khamis"), ("consigneecity", "Khamis Mushait"), ("consigneezipcode", "13958"), ("consigneeprovince", "Asir"))),
                    ("volumes", (("number", "1"), ("prewidth", 50.0), ("prelength", 50.0), ("preheight", 50.0), ("prerweight", 15.55))),
                    ("items", (("number", "1-5"), ("cnname", "手机壳"), ("enname", "iphone case"), ("weight", 1.15), ("quantity", 10), ("price", 5.87), ("declarecurrency", "USD"), ("isbatterys", 0), ("ismagnets", 0), ("isliquids", 0), ("ispowders", 0))),
                ),
            )),
        ): mock_response_data_fail_data,
    },
    ("create_fba_forecast", "post"): {
        (
            ("authorization", (("code", "KJHBA"), ("token", "60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"))),
            ("datas", (
                (
                    ("order", (("channelid", "HK_TNT"), ("customernumber1", "T620200611-1001"), ("number", 5), ("forecastweight", 77.75), ("isbattery", 0), ("countrycode", "RU"), ("consigneename", "Nwabisa Mkaka"), ("consigneeaddress1", "nah Iskan 2 Khamis"), ("consigneecity", "Khamis Mushait"), ("consigneezipcode", "13958"), ("consigneeprovince", "Asir"))),
                    ("volumes", (("number", "1"), ("prewidth", 50.0), ("prelength", 50.0), ("preheight", 50.0), ("prerweight", 15.55)), (("number", "2-5"), ("prewidth", 50.0), ("prelength", 50.0), ("preheight", 50.0), ("prerweight", 15.55))),
                    ("items", (("number", "1-5"), ("cnname", "手机壳"), ("enname", "iphone case"), ("weight", 1.15), ("quantity", 10), ("price", 5.87), ("declarecurrency", "USD"), ("isbatterys", 0), ("ismagnets", 0), ("isliquids", 0), ("ispowders", 0))),
                ),
            )),
        ): {**mock_response_data_success, "msg": "预报成功"}, # 预报接口的成功信息可能不同
    }
}