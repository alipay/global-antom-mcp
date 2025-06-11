from com.alipay.ams.api.request.pay.alipay_refund_query_request import AlipayRefundQueryRequest

from shared.service_base import ServiceBase


class QueryRefundService(ServiceBase):

    def execute(self, request, alipay_sdk_client):

        alipay_refund_query_request = AlipayRefundQueryRequest()
        alipay_refund_query_request.refund_request_id = request.refund_request_id

        return alipay_sdk_client.execute(alipay_refund_query_request)

