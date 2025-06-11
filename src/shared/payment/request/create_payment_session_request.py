
class CreatePaymentSessionRequest:

    def __init__(self):
        self.__payment_request_id = None
        self.__order_amount_currency = None
        self.__order_amount_value = None
        self.__order_description = None
        self.__payment_redirect_url = None
        self.__payment_notify_url = None

    @property
    def payment_request_id(self):
        return self.__payment_request_id

    @payment_request_id.setter
    def payment_request_id(self, value):
        self.__payment_request_id = value

    @property
    def order_amount_currency(self):
        return self.__order_amount_currency

    @order_amount_currency.setter
    def order_amount_currency(self, value):
        self.__order_amount_currency = value

    @property
    def order_amount_value(self):
        return self.__order_amount_value

    @order_amount_value.setter
    def order_amount_value(self, value):
        self.__order_amount_value = value

    @property
    def order_description(self):
        return self.__order_description

    @order_description.setter
    def order_description(self, value):
        self.__order_description = value

    @property
    def payment_redirect_url(self):
        return self.__payment_redirect_url

    @payment_redirect_url.setter
    def payment_redirect_url(self, value):
        self.__payment_redirect_url = value

    @property
    def payment_notify_url(self):
        return self.__payment_notify_url

    @payment_notify_url.setter
    def payment_notify_url(self, value):
        self.__payment_notify_url = value
