import unittest
import time
import uuid
from mangrove import Mangrove, UserCredential, Order
from entity import OrderCallback, Model, NamedModel, MerchantOrder


class TestMangrove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        credential = UserCredential(
            external_id="sbSO9eCvjQkE38hVnrVy4TiD",
            secret="ER3wT3UP05TVEyh8CdMnZsCz5I1j0z"
        )
        cls.mangrove = Mangrove("http://10.0.0.254:4003", credential)

    def test_create_merchant_order(self):
        order = Order(
            amount="1",
            order_callback=OrderCallback(
                endpoint="http://127.0.0.1:8888"
            )
        )
        merchant_order = MerchantOrder(order=order)
        result = self.mangrove.merchant_order.create(merchant_order)
        if result:
            print(f"The code for this order is {result[0].order.code}")
        else:
            print("Error creating merchant order")

    def test_describe_order(self):
        uuid0 = "05bf25dd-103a-4580-96b2-4e30c9736822"
        order = self.mangrove.order.describe(uuid0)
        if order:
            print(f"The code for this order is {order.code}")
        else:
            print("Error describing order")

    def test_update_order(self):
        order = Order(
            model=Model(uuid="05bf25dd-103a-4580-96b2-4e30c9736822"),
            named_model=NamedModel(name=time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        orders = self.mangrove.order.update(order)
        if orders:
            print(f"The code for this order is {orders[0].code}")
        else:
            print("Error updating order")

    def test_delete_order(self):
        try:
            self.mangrove.order.delete(uuid0="15bf25dd-103a-4580-96b2-4e30c9736822")
            print("Order deleted successfully")
        except ValueError as e:
            print(f"Error deleting order: {e}")

    def test_handle_order_callback(self):
        mock_request = {
            "method": "POST",
            "path": "/v1.2/order/callback",
            "headers": {
                "content-type": "application/json",
                "host": "10.0.0.254:4003",
                "x-guarder-id": "sbSO9eCvjQkE38hVnrVy4TiD",
                "x-guarder-signed-at": str(int(time.time() * 1000)),
                "x-guarder-uuid": str(uuid.uuid4()),
                "Authorization": "Signature <correct_signature>"
            },
            "body": {
                "order_transaction_id": "12345",
                "status": "completed",
                "amount": "100",
                "integral_amount": "0",
                "external_id": "ext123",
                "code": "order123",
                "order_callback": {
                    "endpoint": "http://127.0.0.1:8888"
                }
            }
        }
        mock_request["headers"]["Authorization"] = \
            f"Signature {self.mangrove.sign_request(mock_request['method'], mock_request['path'],
                                                    mock_request['headers'], mock_request['body'])}"
        print(mock_request)
        try:
            order = self.mangrove.order.handle_callback(mock_request)
            print(f"The code for this order is {order.code}")
        except ValueError as e:
            print(f"Error handling order callback: {e}")

    def test_summarize_user_integral_amount(self):
        result = self.mangrove.user.summarize_integral_amount()
        for key, value in result.items():
            print(f"{key} → {value}")


if __name__ == "__main__":
    unittest.main()
