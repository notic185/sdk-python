import hashlib
import hmac
import json
import time
import uuid
from typing import Optional, Any, Union, Dict
import requests
from entity import UserCredential, MerchantOrder, Order, UserOrder


class Mangrove:
    def __init__(self, endpoint: str, credential: UserCredential):
        self.endpoint = endpoint
        self.credential = credential
        self.merchant_order = MangroveMerchantOrder(self)
        self.order = MangroveOrder(self)
        self.user = MangroveUser(self)
        self.user_order = MangroveUserOrder(self)

    def request(self, request_method: str, request_path: str, request_payload: Optional[Any] = None) -> Union[Dict, None]:
        request_url = self.endpoint + request_path
        headers = {
            "content-type": "application/json",
            "host": self.endpoint.split('/')[-1],
            "x-guarder-id": self.credential.external_id,
            "x-guarder-signed-at": str(int(time.time() * 1000)),
            "x-guarder-uuid": str(uuid.uuid4())
        }
        headers["Authorization"] = f"Signature {self.sign_request(request_method, request_path, headers,
                                                                  request_payload)}"
        response = requests.request(request_method, request_url, json=request_payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('data')
        else:
            raise Exception(f"Error: {response.json().get('message')}")

    def sign_request(self, request_method: str, request_path: str, headers: Dict,
                     request_payload: Optional[Any] = None) -> str:
        signature_payload = [f"{request_method} {request_path}"]
        for key in ["content-type", "host", "x-guarder-id", "x-guarder-signed-at", "x-guarder-uuid"]:
            signature_payload.append(f"{key}: {headers[key]}")
        signature_payload.append("")
        if request_payload is None:
            signature_payload.append("")
        else:
            # 确保使用紧凑且有序的 JSON 格式
            json_payload = json.dumps(request_payload, separators=(',', ':'), sort_keys=True)
            signature_payload.append(json_payload)
        # 计算签名
        message = '\r\n'.join(signature_payload).encode('utf-8')
        signature = hmac.new(
            self.credential.secret.encode('utf-8'),
            msg=message,
            digestmod=hashlib.sha512
        ).hexdigest()
        return signature


class MangroveMerchantOrder:
    def __init__(self, mangrove: Mangrove):
        self.mangrove = mangrove

    def create(self, merchant_order: MerchantOrder):
        if merchant_order.order.order_callback.endpoint:
            merchant_order.order.order_callback.endpoint = f"v2:{merchant_order.order.order_callback.endpoint}"
        result = self.mangrove.request('PUT', '/v1.2/merchant-order', merchant_order.to_dict())
        return [MerchantOrder(**order) for order in result] if result else []


class MangroveOrder:
    def __init__(self, mangrove: Mangrove):
        self.mangrove = mangrove

    def describe(self, uuid0: str):
        result = self.mangrove.request('GET', f'/v1.2/order/{uuid0}')
        return Order(**result) if result else None

    def update(self, order: Order):
        result = self.mangrove.request('PATCH', f'/v1.2/order/{order.model.uuid}', order.to_dict())
        return [Order(**order) for order in result] if result else []

    def delete(self, uuid0: str):
        self.mangrove.request('DELETE', f'/v1.2/order/{uuid0}')

    def handle_callback(self, request: Dict):
        headers = request.get('headers', {})
        request_payload = request.get('body', {})
        request_signature = self.mangrove.sign_request(request.get('method', 'GET'), request.get('path', ''), headers,
                                                       request_payload)
        if request_signature == headers.get('Authorization', '').split(' ')[1]:
            try:
                return Order(**request_payload)
            except ValueError as e:
                raise e
        else:
            raise ValueError("invalid signature")


class MangroveUser:
    def __init__(self, mangrove: Mangrove):
        self.mangrove = mangrove

    def summarize_integral_amount(self) -> Dict[str, float]:
        result = self.mangrove.request('GET', '/v1.2/user/summarize-integral-amount')
        return result if result else {}


class MangroveUserOrder:
    def __init__(self, mangrove: Mangrove):
        self.mangrove = mangrove

    def create(self, user_orders: UserOrder):
        result = self.mangrove.request('PUT', '/v1.2/user-order', user_orders.to_dict())
        return [UserOrder(**order) for order in result] if result else []
