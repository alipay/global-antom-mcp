import json
import os
import time
import unittest

from dotenv import load_dotenv

from shared.antom_client import AntomClient
from shared.payment.request.create_payment_session_request import CreatePaymentSessionRequest


class TestCreatePaymentSessionService(unittest.TestCase):

    def setUp(self):
        load_dotenv()  # Try to load .env from project root or current working directory
        self.gateway_url = os.environ.get("TEST_GATEWAY_URL", "https://open-sea-global.alipay.com")
        self.client_id = os.environ.get("TEST_CLIENT_ID", "test_client_id_from_env")
        self.merchant_private_key = os.environ.get("TEST_MERCHANT_PRIVATE_KEY", "dummy_private_key_from_env")
        self.alipay_public_key = os.environ.get("TEST_ALIPAY_PUBLIC_KEY", "dummy_public_key_from_env")
        self.payment_notify_url = os.environ.get("TEST_PAYMENT_NOTIFY_URL", "http://dummy_payment_notify_url_from_env.com")

        self.client = AntomClient(self.gateway_url, self.client_id, self.merchant_private_key, self.alipay_public_key)

    def test_create_payment_session(self):
        # Create request
        request = CreatePaymentSessionRequest()
        # Generate a unique payment_request_id using timestamp
        payment_request_id = 'test_payment_request_id_' + str(int(time.time()))
        request.payment_request_id = payment_request_id
        request.order_amount_currency = 'SGD'
        request.order_amount_value = '50'
        request.order_description = 'Test Order'
        # Match the server implementation for redirect and notify URLs
        request.payment_redirect_url = f"http://localhost:8080/index.html?paymentRequestId={payment_request_id}"
        request.payment_notify_url = self.payment_notify_url

        # Execute request
        response = self.client.execute(request)

        # Verify response
        # Basic validation
        self.assertIsNotNone(response)

        # Check that the response is not an error message
        self.assertFalse(isinstance(response, Exception))
        self.assertFalse(isinstance(response, str) and ('error' in response.lower() or 'exception' in response.lower()))

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

        # Check that required fields exist but don't validate their specific values
        # as they are dynamic
        self.assertIn('normalUrl', json_response)
        self.assertIn('paymentSessionData', json_response)
        self.assertIn('paymentSessionExpiryTime', json_response)
        self.assertIn('paymentSessionId', json_response)


if __name__ == '__main__':
    # This allows you to run this test file directly
    unittest.main()
