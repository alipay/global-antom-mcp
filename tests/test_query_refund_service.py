import json
import os
import unittest

from dotenv import load_dotenv

from shared.antom_client import AntomClient
from shared.refund.request.query_refund_request import QueryRefundRequest


class TestQueryRefundService(unittest.TestCase):

    def setUp(self):
        load_dotenv()  # Try to load .env from project root or current working directory
        self.gateway_url = os.environ.get("TEST_GATEWAY_URL", "https://open-sea-global.alipay.com")
        self.client_id = os.environ.get("TEST_CLIENT_ID", "test_client_id_from_env")
        self.merchant_private_key = os.environ.get("TEST_MERCHANT_PRIVATE_KEY", "dummy_private_key_from_env")
        self.alipay_public_key = os.environ.get("TEST_ALIPAY_PUBLIC_KEY", "dummy_public_key_from_env")
        self.payment_notify_url = os.environ.get("TEST_PAYMENT_NOTIFY_URL", "dummy_payment_notify_url_from_env")

        self.client = AntomClient(self.gateway_url, self.client_id, self.merchant_private_key, self.alipay_public_key)

    def test_query_refund(self):
        # Use a refund_request_id that should exist in the system
        # This should be a refund_request_id that was generated when creating a refund
        # for the payment with ID 202505281940108001001882J0236686092
        # For this test, we'll use a hardcoded refund_request_id
        refund_request_id = "7aeb0d38-5def-4b3f-bd5f-800a5f0ae3c8"  # Using a predictable ID based on the payment ID
        # Create request
        request = QueryRefundRequest(refund_request_id=refund_request_id)

        # Execute request
        response = self.client.execute(request)

        # Verify response
        # Basic validation
        self.assertIsNotNone(response)

        # Check that the response is not an error message
        self.assertFalse(isinstance(response, Exception))

        # Print response for debugging
        print(f"Response type: {type(response)}")
        print(f"Response: {response}")

        # Handle JSON string response
        json_response = json.loads(response)

        # Validate the JSON response structure
        self.assertIn('result', json_response)
        self.assertEqual(json_response['result']['resultCode'], 'SUCCESS')
        self.assertEqual(json_response['result']['resultMessage'], 'success.')
        self.assertEqual(json_response['result']['resultStatus'], 'S')

        # Validate refund details
        self.assertEqual(json_response['refundRequestId'], refund_request_id)


if __name__ == '__main__':
    # This allows you to run this test file directly
    unittest.main()
