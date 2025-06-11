
class CreateRefundRequest:

    def __init__(self):
        self.__refund_request_id = None
        self.__payment_id = None
        self.__refund_amount_currency = None
        self.__refund_amount_value = None

    @property
    def refund_request_id(self):
        return self.__refund_request_id

    @refund_request_id.setter
    def refund_request_id(self, value):
        self.__refund_request_id = value

    @property
    def payment_id(self):
        return self.__payment_id

    @payment_id.setter
    def payment_id(self, value):
        self.__payment_id = value

    @property
    def refund_amount_currency(self):
        return self.__refund_amount_currency

    @refund_amount_currency.setter
    def refund_amount_currency(self, value):
        self.__refund_amount_currency = value

    @property
    def refund_amount_value(self):
        return self.__refund_amount_value

    @refund_amount_value.setter
    def refund_amount_value(self, value):
        self.__refund_amount_value = value
