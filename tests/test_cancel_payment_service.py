import json
import os
import unittest

from dotenv import load_dotenv

from shared.antom_client import AntomClient
from shared.payment.request.cancel_payment_request import CancelPaymentRequest


class TestCancelPaymentService(unittest.TestCase):

    def setUp(self):
        load_dotenv()  # Try to load .env from project root or current working directory
        self.gateway_url = os.environ.get("TEST_GATEWAY_URL", "https://open-sea-global.alipay.com")
        self.client_id = os.environ.get("TEST_CLIENT_ID", "test_client_id_from_env")
        self.merchant_private_key = os.environ.get("TEST_MERCHANT_PRIVATE_KEY", "dummy_private_key_from_env")
        self.alipay_public_key = os.environ.get("TEST_ALIPAY_PUBLIC_KEY", "dummy_public_key_from_env")
        self.payment_notify_url = os.environ.get("TEST_PAYMENT_NOTIFY_URL", "dummy_payment_notify_url_from_env")

        self.client = AntomClient(self.gateway_url, self.client_id, self.merchant_private_key, self.alipay_public_key)

    def test_cancel_payment(self):
        # Use the provided payment_request_id
        payment_request_id = 'c8421285-8849-4504-8375-6d3968b9e934'
        # Create request
        request = CancelPaymentRequest(payment_request_id=payment_request_id)

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

        # Handle different response formats based on the actual API response
        json_response = json.loads(response)

        # Validate only the non-dynamic fields in the response
        self.assertIn('result', json_response)
        self.assertEqual(json_response['result']['resultCode'], 'SUCCESS')
        self.assertEqual(json_response['result']['resultMessage'], 'success.')
        self.assertEqual(json_response['result']['resultStatus'], 'S')

        # Check that the payment_request_id matches
        self.assertEqual(json_response.get('paymentRequestId'), payment_request_id)


if __name__ == '__main__':
    # This allows you to run this test file directly
    unittest.main()
