import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from com.alipay.ams.api.exception.exception import AlipayApiException
from mcp.server import FastMCP

from shared.antom_client import AntomClient
from shared.payment.request.cancel_payment_request import CancelPaymentRequest
from shared.payment.request.create_payment_session_request import CreatePaymentSessionRequest
from shared.payment.request.query_payment_request import QueryPaymentRequest
from shared.refund.request.create_refund_request import CreateRefundRequest
from shared.refund.request.query_refund_request import QueryRefundRequest


def main():

    # env config
    env_vars_config = {
        "GATEWAY_URL": "https://open-sea-global.alipay.com",
        "CLIENT_ID": "",
        "MERCHANT_PRIVATE_KEY": "",
        "ALIPAY_PUBLIC_KEY": "",
        "PAYMENT_REDIRECT_URL": "",
        "PAYMENT_NOTIFY_URL": "http://localhost:8080/notify"
    }

    account_data = {}
    missing_vars = []

    for var_name, default_value in env_vars_config.items():
        var_value = os.getenv(var_name)
        if var_value is None:
            if default_value is not None:
                print(f"Warning: Environment variable {var_name} not set. Using default value: '{default_value}'")
                account_data[var_name.lower()] = default_value  # Convert keys to lowercase to match Account attributes
            else:
                missing_vars.append(var_name)
        else:
            account_data[var_name.lower()] = var_value

    if missing_vars:
        print(f"Error: Required environment variables are not set: {', '.join(missing_vars)}")
        print("Please set these environment variables before running the application.")
        sys.exit(1)  # Exit program with error code 1

    antom_client = AntomClient(gateway_url=account_data.get('gateway_url'),
                               client_id=account_data.get('client_id'),
                               merchant_private_key=account_data.get('merchant_private_key'),
                               alipay_public_key=account_data.get('alipay_public_key'))

    @asynccontextmanager
    async def antom_lifespan(server: FastMCP) -> AsyncIterator[dict]:
        """Lifespan context manager for the mcp server."""
        yield {"client": antom_client}

    mcp = FastMCP("antom-mcp", lifespan=antom_lifespan)

    @mcp.tool()
    def create_payment_session(payment_request_id: str,
                               order_amount_currency: str,
                               order_amount_value: int,
                               order_description: str) -> str:
        """ The tool is used to create a payment session which helps you complete the payment process and eliminate intermediate page redirections throughout the entire payment process.

        Args:
            payment_request_id: The unique ID assigned by a merchant to identify a payment request. Maximum length: 64 characters
            order_amount_currency: The transaction currency that is specified in the contract. A 3-letter currency code that follows the ISO 4217 standard.Maximum length: 3 characters
            order_amount_value: The amount to charge as a positive integer in the smallest currency unit. (That is, 100 cents to charge $1.00, or 100 to charge JPY 100, a 0-decimal currency).Value range: 1 - unlimited
            order_description: Summary description of the order, which is used for user consumption records display or other further actions.Maximum length: 256 characters
        """
        try:
            create_payment_session_request = CreatePaymentSessionRequest()
            create_payment_session_request.payment_request_id = payment_request_id
            create_payment_session_request.order_amount_currency = order_amount_currency
            create_payment_session_request.order_amount_value = order_amount_value
            create_payment_session_request.order_description = order_description
            create_payment_session_request.payment_redirect_url = account_data.get('payment_redirect_url') or "/"
            create_payment_session_request.payment_notify_url = account_data.get('payment_notify_url')

            return antom_client.execute(create_payment_session_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def query_payment_detail(payment_request_id: str) -> str:
        """ The tool is used to inquire about the transaction status and other information about a previously submitted payment request.

        Args:
            payment_request_id: The unique ID that is assigned by a merchant to identify a payment request.Maximum length: 64 characters
        """
        try:
            query_payment_request = QueryPaymentRequest(payment_request_id=payment_request_id)
            return antom_client.execute(query_payment_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def cancel_payment(payment_request_id: str) -> str:
        """ The tool is used to cancel the payment if the payment result is not returned after a long time. The cancellation cannot be performed if being out of the cancellable period specified in the contract.

        Args:
            payment_request_id: The unique ID that is assigned by a merchant to identify a payment request.Maximum length: 64 characters
        """
        try:
            cancel_payment_request = CancelPaymentRequest(payment_request_id=payment_request_id)
            return antom_client.execute(cancel_payment_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def create_refund(refund_request_id: str,
                      payment_id: str,
                      refund_amount_currency: str,
                      refund_amount_value: str, ) -> str:
        """ The tool is used to initiate a refund against a successful payment. The refund can be full or partial. A transaction can have multiple refunds as long as the total refund amount is less than or equal to the original transaction amount. If the refund request is out of the refund window determined in the contract, the refund request will be declined.

        Args:
            refund_request_id: The unique ID assigned by the merchant to identify a refund request.Maximum length: 64 characters
            payment_id: The unique ID assigned by Antom for the original payment to be refunded.Maximum length: 64 characters
            refund_amount_currency: The currency used for the corresponding payment of the refund. The value is a 3-letter currency code that follows the ISO 4217 standard.
            refund_amount_value: The amount to charge as a positive integer in the smallest currency unit. (That is, 100 cents to charge $1.00, or 100 to charge JPY 100, a 0-decimal currency).Value range: 1 - unlimited
        """
        try:
            create_refund_request = CreateRefundRequest()
            create_refund_request.refund_request_id = refund_request_id
            create_refund_request.payment_id = payment_id
            create_refund_request.refund_amount_currency = refund_amount_currency
            create_refund_request.refund_amount_value = refund_amount_value
            return antom_client.execute(create_refund_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def query_refund_detail(refund_request_id: str) -> str:
        """ The tool is used to inquire about the refund status of a previously submitted refund request.

        Args:
            refund_request_id: The unique ID assigned by the merchant to identify a refund request.Maximum length: 64 characters
        """
        try:
            query_refund_request = QueryRefundRequest(refund_request_id=refund_request_id)
            return antom_client.execute(query_refund_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    mcp.run("stdio")


if __name__ == "__main__":
    main()
