from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict) -> bool: ...

    @abstractmethod
    def handle(self, update: dict) -> bool:
        """
        return optinons:
        - true - signal for dispantcher to continue processing
        - false - signal for dispatcher to STOP processing
        """
        pass