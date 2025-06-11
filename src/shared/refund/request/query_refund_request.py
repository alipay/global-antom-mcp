
class QueryRefundRequest:

    def __init__(self, refund_request_id: str):
        self.__refund_request_id = refund_request_id

    @property
    def refund_request_id(self):
        return self.__refund_request_id

    @refund_request_id.setter
    def refund_request_id(self, value):
        self.__refund_request_id = value
