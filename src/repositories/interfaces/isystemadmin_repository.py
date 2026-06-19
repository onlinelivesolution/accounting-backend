from abc import ABC, abstractmethod


class ISystemAdminRepository(ABC):

    @abstractmethod
    async def get_by_username(self, username: str):
        pass

    @abstractmethod
    async def update(self, user):
        pass
