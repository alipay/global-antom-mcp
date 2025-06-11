import json
import os
import unittest

from dotenv import load_dotenv

from shared.antom_client import AntomClient
from shared.payment.request.query_payment_request import QueryPaymentRequest


class TestQueryPaymentService(unittest.TestCase):

    def setUp(self):
        load_dotenv()  # Try to load .env from project root or current working directory
        self.gateway_url = os.environ.get("TEST_GATEWAY_URL", "https://open-sea-global.alipay.com")
        self.client_id = os.environ.get("TEST_CLIENT_ID", "test_client_id_from_env")
        self.merchant_private_key = os.environ.get("TEST_MERCHANT_PRIVATE_KEY", "dummy_private_key_from_env")
        self.alipay_public_key = os.environ.get("TEST_ALIPAY_PUBLIC_KEY", "dummy_public_key_from_env")
        self.payment_notify_url = os.environ.get("TEST_PAYMENT_NOTIFY_URL", "dummy_payment_notify_url_from_env")

        self.client = AntomClient(self.gateway_url, self.client_id, self.merchant_private_key, self.alipay_public_key)

    def test_query_payment(self):
        # Create request
        # Use a payment_request_id that should exist in the system
        # In a real test, you might want to create a payment first and then query it
        payment_request_id = 'HZPOEM202310251015'
        request = QueryPaymentRequest(payment_request_id=payment_request_id)

        # Execute request
        response = self.client.execute(request)

        # Verify response
        # Basic validation
        self.assertIsNotNone(response)

        # Check that the response is not an error message
        self.assertFalse(isinstance(response, Exception))

        # We expect a JSON string response, so we only check for error messages
        # but don't fail if it's a valid JSON string
        if isinstance(response, str):
            # Only check for simple error messages, not JSON strings that might contain 'error' as part of valid data
            if not response.startswith('{'): 
                self.assertFalse('error' in response.lower() or 'exception' in response.lower())

        # Print response for debugging
        print(f"Response type: {type(response)}")
        print(f"Response: {response}")

        # Handle JSON string response
        json_response = json.loads(response)

        # Validate the JSON response structure based on the sample provided
        self.assertIn('result', json_response)
        self.assertEqual(json_response['result']['resultCode'], 'SUCCESS')
        self.assertEqual(json_response['result']['resultMessage'], 'success.')
        self.assertEqual(json_response['result']['resultStatus'], 'S')

        # Validate payment details
        self.assertEqual(json_response['paymentRequestId'], payment_request_id)
        self.assertEqual(json_response['paymentStatus'], 'SUCCESS')
        self.assertEqual(json_response['paymentResultCode'], 'SUCCESS')
        self.assertEqual(json_response['paymentMethodType'], 'RABBIT_LINE_PAY')

        # Validate payment amounts
        self.assertEqual(json_response['paymentAmount']['currency'], 'CNY')
        self.assertEqual(json_response['paymentAmount']['value'], '300')

        # Validate transactions if present
        if 'transactions' in json_response and json_response['transactions']:
            transaction = json_response['transactions'][0]
            self.assertEqual(transaction['transactionStatus'], 'SUCCESS')
            self.assertEqual(transaction['transactionResult']['resultStatus'], 'S')


if __name__ == '__main__':
    # This allows you to run this test file directly
    unittest.main()
