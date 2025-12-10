#!/usr/bin/env python
# encoding: utf-8
# @Time   : 2025/12/8 18:41
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : mock_data.py
import datetime
from typing import Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type

mock_time = datetime.datetime.now().isoformat()

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    ("server_status", "get"): {
        (("keyword", "123456"),): dict(Status="normal", time=mock_time),
        (("keyword", "11222"),): dict(Status="error code", time=mock_time),
        (("keyword", ""),): dict(Status="error code for None", time=mock_time),
    },
    ("query_channel", "post"): {
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
        ): dict(
            code=0,
            msg="调用成功",
            data=[
                {
                    "channelid": "CN_EMS",
                    "channeltype": "快递",
                    "channelname": "中国邮政",
                    "channelnamecn": "中国邮政",
                    "channelnameen": "China Post",
                },
                {
                    "channelid": "HK_TNT",
                    "channeltype": "专线",
                    "channelname": "香港TNT",
                    "channelnamecn": "香港TNT",
                    "channelnameen": "Hong Kong TNT",
                },
                {
                    "channelid": "MS_KQ",
                    "channeltype": "专线",
                    "channelname": "美森快船",
                    "channelnamecn": "美森快船",
                    "channelnameen": "Mason Clippers",
                },
            ],
        ),
        (
            (
                "authorization",
                (
                    ("code", "ERROR"),
                    ("token", "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
                ),
            ),
        ): dict(
            code=1001,
            msg="授权失败，请检查code和token",
            data=[],
        ),
        (("authorization", (("code", "KJHBA"), ("token", "short"))),): dict(
            code=400,
            msg="请求参数校验失败：token长度不足50",
            data=[],
        ),
    },
}
# 示例请求数据
mock_request_data_success = {
    "authorization": {
        "code": "KJHBA",
        "token": "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas",
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
                "forecastweight": 77.75,  # 15.55 * 5
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
                    "prerweight": 15.55,
                },
                {
                    "number": "2-5",
                    "customerchildnumber": "CH-85120-1002",
                    "prewidth": 50.0,
                    "prelength": 50.0,
                    "preheight": 50.0,
                    "prerweight": 15.55,
                },
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
            ],
        }
    ],
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
                {
                    "customernumber": "CH-85120-1001",
                    "systemnumber": "1591857709631-1",
                    "tracknumber": "1Z76V3R40448621361",
                },
                {
                    "customernumber": "CH-85120-1002",
                    "systemnumber": "1591857709631-2",
                    "tracknumber": "1Z76V3R40448621362",
                },
                {
                    "customernumber": "CH-85120-1003",
                    "systemnumber": "1591857709631-3",
                    "tracknumber": "1Z76V3R40448621363",
                },
                {
                    "customernumber": "CH-85120-1004",
                    "systemnumber": "1591857709631-4",
                    "tracknumber": "1Z76V3R40448621363",
                },
                {
                    "customernumber": "CH-85120-1005",
                    "systemnumber": "1591857709631-5",
                    "tracknumber": "1Z76V3R40448621363",
                },
            ],
        }
    ],
}

mock_request_data_fail_auth = {
    "authorization": {
        "code": "ERROR",
        "token": "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    },
    "datas": [
        # 即使数据正确，授权失败也会导致调用失败
        mock_request_data_success["datas"][0]
    ],
}

mock_response_data_fail_auth = {
    "code": 1001,
    "msg": "授权失败，请检查code和token",
    "data": [],
}

mock_request_data_fail_data = {
    "authorization": {
        "code": "KJHBA",
        "token": "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas",
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
                    "prerweight": 15.55,
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
            ],
        }
    ],
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
    ],
}

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    **MOCK_DATA,
    ("create_fba_draft", "post"): {
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
            (
                "datas",
                (
                    (
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("customernumber1", "T620200611-1001"),
                                ("number", 5),
                                ("forecastweight", 77.75),
                                ("isbattery", 0),
                                ("countrycode", "RU"),
                                ("consigneename", "Nwabisa Mkaka"),
                                ("consigneeaddress1", "nah Iskan 2 Khamis"),
                                ("consigneecity", "Khamis Mushait"),
                                ("consigneezipcode", "13958"),
                                ("consigneeprovince", "Asir"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("number", "1"),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                            (
                                ("number", "2-5"),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("number", "1-5"),
                                ("cnname", "手机壳"),
                                ("enname", "iphone case"),
                                ("weight", 1.15),
                                ("quantity", 10),
                                ("price", 5.87),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): mock_response_data_success,
        (
            (
                "authorization",
                (
                    ("code", "ERROR"),
                    ("token", "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
                ),
            ),
            # 简化请求数据，只保留必须字段，以匹配授权失败的用例
            (
                "datas",
                (
                    (
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("customernumber1", "FAIL_AUTH"),
                                ("number", 1),
                                ("forecastweight", 1.0),
                                ("isbattery", 0),
                                ("countrycode", "CN"),
                                ("consigneename", "Test"),
                                ("consigneeaddress1", "Test Addr"),
                                ("consigneecity", "Test City"),
                                ("consigneezipcode", "100000"),
                                ("consigneeprovince", "Test Prov"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("number", "1"),
                                ("prewidth", 10.0),
                                ("prelength", 10.0),
                                ("preheight", 10.0),
                                ("prerweight", 1.0),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("number", "1"),
                                ("cnname", "测试品"),
                                ("enname", "Test Item"),
                                ("weight", 0.1),
                                ("quantity", 1),
                                ("price", 1.0),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): mock_response_data_fail_auth,
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
            (
                "datas",
                (
                    (
                        # customernumber1 缺失，模拟数据校验失败
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("number", 5),
                                ("forecastweight", 77.75),
                                ("isbattery", 0),
                                ("countrycode", "RU"),
                                ("consigneename", "Nwabisa Mkaka"),
                                ("consigneeaddress1", "nah Iskan 2 Khamis"),
                                ("consigneecity", "Khamis Mushait"),
                                ("consigneezipcode", "13958"),
                                ("consigneeprovince", "Asir"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("number", "1"),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("number", "1-5"),
                                ("cnname", "手机壳"),
                                ("enname", "iphone case"),
                                ("weight", 1.15),
                                ("quantity", 10),
                                ("price", 5.87),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): mock_response_data_fail_data,
    },
    ("create_fba_forecast", "post"): {
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
            (
                "datas",
                (
                    (
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("customernumber1", "T620200611-1001"),
                                ("number", 5),
                                ("forecastweight", 77.75),
                                ("isbattery", 0),
                                ("countrycode", "RU"),
                                ("consigneename", "Nwabisa Mkaka"),
                                ("consigneeaddress1", "nah Iskan 2 Khamis"),
                                ("consigneecity", "Khamis Mushait"),
                                ("consigneezipcode", "13958"),
                                ("consigneeprovince", "Asir"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("number", "1"),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                            (
                                ("number", "2-5"),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("number", "1-5"),
                                ("cnname", "手机壳"),
                                ("enname", "iphone case"),
                                ("weight", 1.15),
                                ("quantity", 10),
                                ("price", 5.87),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): {
            **mock_response_data_success,
            "msg": "预报成功",
        },  # 预报接口的成功信息可能不同
    },
}

# 示例请求数据
mock_request_data_success = {
    "authorization": {
        "code": "KJHBA",
        "token": "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas",
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
                "forecastweight": 77.75,  # 15.55 * 5
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
                    "customerchildnumber": "CH-85120-1001",
                    "prenum": 5,
                    "prewidth": 50.0,
                    "prelength": 50.0,
                    "preheight": 50.0,
                    "prerweight": 15.55,
                }
            ],
            "items": [
                {
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
            ],
        }
    ],
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
            "isRemote": True,
            "childs": [
                {
                    "customernumber": "CH-85120-1001",
                    "systemnumber": "1591857709631-1",
                    "tracknumber": "1Z76V3R40448621361",
                },
                {
                    "customernumber": "CH-85120-1002",
                    "systemnumber": "1591857709631-2",
                    "tracknumber": "1Z76V3R40448621362",
                },
                {
                    "customernumber": "CH-85120-1003",
                    "systemnumber": "1591857709631-3",
                    "tracknumber": "1Z76V3R40448621363",
                },
                {
                    "customernumber": "CH-85120-1004",
                    "systemnumber": "1591857709631-4",
                    "tracknumber": "1Z76V3R40448621363",
                },
                {
                    "customernumber": "CH-85120-1005",
                    "systemnumber": "1591857709631-5",
                    "tracknumber": "1Z76V3R40448621363",
                },
            ],
        }
    ],
}

mock_request_data_fail_auth = {
    "authorization": {
        "code": "ERROR",
        "token": "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    },
    "datas": [
        # 即使数据正确，授权失败也会导致调用失败
        mock_request_data_success["datas"][0]
    ],
}

mock_response_data_fail_auth = {
    "code": 1001,
    "msg": "授权失败，请检查code和token",
    "data": [],
}

mock_request_data_fail_data = {
    "authorization": {
        "code": "KJHBA",
        "token": "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas",
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
                    "customerchildnumber": "CH-85120-1001",
                    "prenum": 5,
                    "prewidth": 50.0,
                    "prelength": 50.0,
                    "preheight": 50.0,
                    "prerweight": 15.55,
                }
            ],
            "items": [
                {
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
            ],
        }
    ],
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
            "shortnumber": None,
            "isRemote": False,
            "childs": None,
        }
    ],
}

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    **MOCK_DATA,
    ("create_order_draft", "post"): {
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
            (
                "datas",
                (
                    (
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("customernumber1", "T620200611-1001"),
                                ("number", 5),
                                ("forecastweight", 77.75),
                                ("isbattery", 0),
                                ("countrycode", "RU"),
                                ("consigneename", "Nwabisa Mkaka"),
                                ("consigneeaddress1", "nah Iskan 2 Khamis"),
                                ("consigneecity", "Khamis Mushait"),
                                ("consigneezipcode", "13958"),
                                ("consigneeprovince", "Asir"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("customerchildnumber", "CH-85120-1001"),
                                ("prenum", 5),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("cnname", "手机壳"),
                                ("enname", "iphone case"),
                                ("weight", 1.15),
                                ("quantity", 10),
                                ("price", 5.87),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): mock_response_data_success,
        (
            (
                "authorization",
                (
                    ("code", "ERROR"),
                    ("token", "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
                ),
            ),
            # 简化请求数据，只保留必须字段，以匹配授权失败的用例
            (
                "datas",
                (
                    (
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("customernumber1", "FAIL_AUTH"),
                                ("number", 1),
                                ("forecastweight", 1.0),
                                ("isbattery", 0),
                                ("countrycode", "CN"),
                                ("consigneename", "Test"),
                                ("consigneeaddress1", "Test Addr"),
                                ("consigneecity", "Test City"),
                                ("consigneezipcode", "100000"),
                                ("consigneeprovince", "Test Prov"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("prenum", 1),
                                ("prewidth", 10.0),
                                ("prelength", 10.0),
                                ("preheight", 10.0),
                                ("prerweight", 1.0),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("cnname", "测试品"),
                                ("enname", "Test Item"),
                                ("weight", 0.1),
                                ("quantity", 1),
                                ("price", 1.0),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): mock_response_data_fail_auth,
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
            (
                "datas",
                (
                    (
                        # customernumber1 缺失，模拟数据校验失败
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("number", 5),
                                ("forecastweight", 77.75),
                                ("isbattery", 0),
                                ("countrycode", "RU"),
                                ("consigneename", "Nwabisa Mkaka"),
                                ("consigneeaddress1", "nah Iskan 2 Khamis"),
                                ("consigneecity", "Khamis Mushait"),
                                ("consigneezipcode", "13958"),
                                ("consigneeprovince", "Asir"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("customerchildnumber", "CH-85120-1001"),
                                ("prenum", 5),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("cnname", "手机壳"),
                                ("enname", "iphone case"),
                                ("weight", 1.15),
                                ("quantity", 10),
                                ("price", 5.87),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): mock_response_data_fail_data,
    },
    ("create_order_forecast", "post"): {
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
            (
                "datas",
                (
                    (
                        (
                            "order",
                            (
                                ("channelid", "HK_TNT"),
                                ("customernumber1", "T620200611-1002"),
                                ("number", 5),
                                ("forecastweight", 77.75),
                                ("isbattery", 0),
                                ("countrycode", "RU"),
                                ("consigneename", "Nwabisa Mkaka"),
                                ("consigneeaddress1", "nah Iskan 2 Khamis"),
                                ("consigneecity", "Khamis Mushait"),
                                ("consigneezipcode", "13958"),
                                ("consigneeprovince", "Asir"),
                            ),
                        ),
                        (
                            "volumes",
                            (
                                ("customerchildnumber", "CH-85120-1001"),
                                ("prenum", 5),
                                ("prewidth", 50.0),
                                ("prelength", 50.0),
                                ("preheight", 50.0),
                                ("prerweight", 15.55),
                            ),
                        ),
                        (
                            "items",
                            (
                                ("cnname", "手机壳"),
                                ("enname", "iphone case"),
                                ("weight", 1.15),
                                ("quantity", 10),
                                ("price", 5.87),
                                ("declarecurrency", "USD"),
                                ("isbatterys", 0),
                                ("ismagnets", 0),
                                ("isliquids", 0),
                                ("ispowders", 0),
                            ),
                        ),
                    ),
                ),
            ),
        ): {
            **mock_response_data_success,
            "msg": "预报成功",
            "data": [
                {
                    **mock_response_data_success["data"][0],
                    "customernumber": "T620200611-1002",
                }
            ],
        },  # 预报接口的成功信息和运单号可能不同
    },
}

MOCK_DATA: Dict[Tuple[str, str], Any] = {
    **MOCK_DATA,
    ("query_currency", "post"): {
        (
            (
                "authorization",
                (
                    ("code", "KJHBA"),
                    ("token", "c60bf762-01f7-470e-8c8f-acde06c81fedaabbvvasdasdas"),
                ),
            ),
        ): dict(
            code=0,
            msg="调用成功",
            data=[
                {"code": "CNY", "cnname": "人民币", "enname": "CNY"},
                {"code": "HKG", "cnname": "港币", "enname": "HKD"},
                {"code": "USD", "cnname": "美元", "enname": "USD"},
                {"code": "EUR", "cnname": "欧元", "enname": "EUR"},
                {"code": "GBP", "cnname": "英镑", "enname": "GBP"},
            ],
        ),
        (
            (
                "authorization",
                (
                    ("code", "ERROR"),
                    ("token", "invalid-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
                ),
            ),
        ): dict(
            code=1001,
            msg="授权失败，请检查code和token",
            data=[],
        ),
        (("authorization", (("code", "KJHBA"), ("token", "short"))),): dict(
            code=400,
            msg="请求参数校验失败：token长度不足50",
            data=[],
        ),
    },
}
