from abc import ABC, abstractmethod

class IClosingService(ABC):

    @abstractmethod
    async def post_closing_journal(self, closing_date):
        pass
