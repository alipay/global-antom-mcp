from abc import ABC, abstractmethod


class ServiceBase(ABC):

    @abstractmethod
    def execute(self, request, alipay_sdk_client):
        pass
