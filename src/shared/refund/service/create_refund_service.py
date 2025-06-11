from com.alipay.ams.api.model.amount import Amount
from com.alipay.ams.api.request.pay.alipay_refund_request import AlipayRefundRequest

from shared.service_base import ServiceBase


class CreateRefundService(ServiceBase):

    def execute(self, request, alipay_sdk_client):

        alipay_refund_request = AlipayRefundRequest()
        alipay_refund_request.refund_request_id = request.refund_request_id
        alipay_refund_request.payment_id = request.payment_id
        refund_amount = Amount(currency=request.refund_amount_currency, value=str(request.refund_amount_value))
        alipay_refund_request.refund_amount = refund_amount

        return alipay_sdk_client.execute(alipay_refund_request)
