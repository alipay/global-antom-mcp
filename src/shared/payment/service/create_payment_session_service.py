import time

from com.alipay.ams.api.model.amount import Amount
from com.alipay.ams.api.model.buyer import Buyer
from com.alipay.ams.api.model.order import Order
from com.alipay.ams.api.request.pay.alipay_create_session_request import AlipayCreateSessionRequest

from shared.service_base import ServiceBase


class CreatePaymentSessionService(ServiceBase):

    def execute(self, request, alipay_sdk_client):

        alipay_create_session_request = AlipayCreateSessionRequest()
        alipay_create_session_request.product_code = "CASHIER_PAYMENT"
        alipay_create_session_request.product_scene = "CHECKOUT_PAYMENT"
        alipay_create_session_request.payment_request_id = request.payment_request_id

        order = Order()
        amount = Amount(currency=request.order_amount_currency, value=str(request.order_amount_value))
        order.order_amount = amount
        order.order_description = request.order_description
        buyer = Buyer()
        buyer.reference_buyer_id = str(int(time.time()))
        order.buyer = buyer
        alipay_create_session_request.order = order
        alipay_create_session_request.payment_amount = amount
        alipay_create_session_request.payment_redirect_url = request.payment_redirect_url
        alipay_create_session_request.payment_notify_url = request.payment_notify_url

        return alipay_sdk_client.execute(alipay_create_session_request)
