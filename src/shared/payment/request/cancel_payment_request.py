

class CancelPaymentRequest:

    def __init__(self, payment_request_id: str):
        self.__payment_request_id = payment_request_id

    @property
    def payment_request_id(self):
        return self.__payment_request_id

    @payment_request_id.setter
    def payment_request_id(self, value):
        self.__payment_request_id = value
