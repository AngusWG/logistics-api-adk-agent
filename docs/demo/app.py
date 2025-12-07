#!/usr/bin/env python
# encoding: utf-8
# @Time   : $DATE.get('yyyy-M-d') 22:57
# @author : zza
# @Email  : z740713651@outlook.com
# @File   : app.py
# app.py (Flask Mock API Server)
from flask import Flask, jsonify, request

app = Flask(__name__)

# 模拟的订单状态数据库
MOCK_ORDERS = {
    "12345": {
        "status": "In Transit",
        "location": "Shanghai Hub",
        "estimated_delivery": "2025-12-15",
    },
    "67890": {
        "status": "Delivered",
        "location": "Los Angeles",
        "estimated_delivery": "2025-12-01",
    },
}


@app.route("/api/shipment/status/<order_id>", methods=["GET"])
def get_shipment_status(order_id):
    """模拟查询订单状态的API"""
    print(f"Flask API: Received status request for order {order_id}")
    if order_id in MOCK_ORDERS:
        return jsonify(
            {"success": True, "order_id": order_id, "data": MOCK_ORDERS[order_id]}
        )
    else:
        return jsonify({"success": False, "error": "Order not found"}), 404


@app.route("/api/shipment/create", methods=["POST"])
def create_shipment():
    """模拟创建新货运单的API"""
    data = request.json
    origin = data.get("origin")
    destination = data.get("destination")

    if not origin or not destination:
        return (
            jsonify({"success": False, "error": "Missing origin or destination"}),
            400,
        )

    # 模拟生成一个新的货运单号
    new_shipment_id = "SHIPMENT-" + str(hash(origin + destination) % 10000)

    print(
        f"Flask API: Created shipment {new_shipment_id} from {origin} to {destination}"
    )

    return jsonify(
        {
            "success": True,
            "shipment_id": new_shipment_id,
            "origin": origin,
            "destination": destination,
            "status": "Pending Creation",
        }
    )


if __name__ == "__main__":
    # 注意: 生产环境请勿使用 debug=True
    print("--- 启动 Flask Mock API 服务 (端口 5000) ---")
    app.run(port=5000, debug=True, use_reloader=False)
