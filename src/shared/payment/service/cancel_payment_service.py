from com.alipay.ams.api.request.pay.alipay_pay_cancel_request import AlipayPayCancelRequest

from shared.service_base import ServiceBase


class CancelPaymentService(ServiceBase):

    def execute(self, request, alipay_sdk_client):

        alipay_pay_cancel_request = AlipayPayCancelRequest()
        alipay_pay_cancel_request.payment_request_id = request.payment_request_id

        return alipay_sdk_client.execute(alipay_pay_cancel_request)

