import os
import unittest
import uuid

from dotenv import load_dotenv

from shared.antom_client import AntomClient
from shared.refund.request.create_refund_request import CreateRefundRequest


class TestCreateRefundService(unittest.TestCase):

    def setUp(self):
        load_dotenv()  # Try to load .env from project root or current working directory
        self.gateway_url = os.environ.get("TEST_GATEWAY_URL", "https://open-sea-global.alipay.com")
        self.client_id = os.environ.get("TEST_CLIENT_ID", "test_client_id_from_env")
        self.merchant_private_key = os.environ.get("TEST_MERCHANT_PRIVATE_KEY", "dummy_private_key_from_env")
        self.alipay_public_key = os.environ.get("TEST_ALIPAY_PUBLIC_KEY", "dummy_public_key_from_env")
        self.payment_notify_url = os.environ.get("TEST_PAYMENT_NOTIFY_URL", "dummy_payment_notify_url_from_env")

        self.client = AntomClient(self.gateway_url, self.client_id, self.merchant_private_key, self.alipay_public_key)

    def test_create_refund(self):
        # Create request
        request = CreateRefundRequest()
        
        # Set the payment_id as specified in the issue description
        payment_id = '202505281940108001001882J0236686092'
        request.payment_id = payment_id
        
        # Generate a unique refund request ID
        refund_request_id = str(uuid.uuid4())
        request.refund_request_id = refund_request_id
        
        # Set the refund amount to 0.1 as specified in the issue description
        request.refund_amount_currency = 'SGD'  # Assuming CNY as the currency
        request.refund_amount_value = 5

        # Execute request
        response = self.client.execute(request)

        # Verify response
        # Basic validation
        self.assertIsNotNone(response)


if __name__ == '__main__':
    # This allows you to run this test file directly
    unittest.main()
