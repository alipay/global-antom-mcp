from com.alipay.ams.api.default_alipay_client import DefaultAlipayClient

from shared.payment.request.cancel_payment_request import CancelPaymentRequest
from shared.payment.request.create_payment_session_request import CreatePaymentSessionRequest
from shared.payment.request.query_payment_request import QueryPaymentRequest
from shared.payment.service.cancel_payment_service import CancelPaymentService
from shared.payment.service.create_payment_session_service import CreatePaymentSessionService
from shared.payment.service.query_payment_service import QueryPaymentService
from shared.refund.request.create_refund_request import CreateRefundRequest
from shared.refund.request.query_refund_request import QueryRefundRequest
from shared.refund.service.create_refund_service import CreateRefundService
from shared.refund.service.query_refund_service import QueryRefundService


class AntomClient:
    def __init__(self, gateway_url: str, client_id: str, merchant_private_key: str, alipay_public_key: str):
        self.__service_map = {
            CreatePaymentSessionRequest: CreatePaymentSessionService(),
            QueryPaymentRequest:  QueryPaymentService(),
            CancelPaymentRequest: CancelPaymentService(),
            CreateRefundRequest: CreateRefundService(),
            QueryRefundRequest: QueryRefundService()
        }
        self.__sdk_client = DefaultAlipayClient(gateway_url=gateway_url,
                                                client_id=client_id,
                                                merchant_private_key=merchant_private_key,
                                                alipay_public_key=alipay_public_key)

    def execute(self, request):
        request_type = type(request)
        if handler := self.__service_map.get(request_type):
            return handler.execute(request, self.__sdk_client)
        raise ValueError(f"No matching service handler found, request type:{request_type.__name__}")
