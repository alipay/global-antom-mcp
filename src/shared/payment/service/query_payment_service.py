from com.alipay.ams.api.request.pay.alipay_pay_query_request import AlipayPayQueryRequest

from shared.service_base import ServiceBase


class QueryPaymentService(ServiceBase):

    def execute(self, request, alipay_sdk_client):

        alipay_pay_query_request = AlipayPayQueryRequest()
        alipay_pay_query_request.payment_request_id = request.payment_request_id

        return alipay_sdk_client.execute(alipay_pay_query_request)
