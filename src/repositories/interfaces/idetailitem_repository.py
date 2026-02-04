from abc import ABC, abstractmethod
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem
from src.models.accountingperiod import AccountingPeriod
from src.schemas.detailitemautocreate_schema import DetailItemAutoCreateRequest


class IDetailItemRepository(ABC):

    # -------------------------------
    # Control Item
    # -------------------------------
    @abstractmethod
    async def get_control_by_name(self, name: str) -> ControlItem | None:
        pass

    # -------------------------------
    # Reporting Item
    # -------------------------------
    @abstractmethod
    async def get_reporting_by_name(
        self,
        name: str,
        control_code: str
    ) -> ReportingItem | None:
        pass

    # -------------------------------
    # Detail Item
    # -------------------------------
    @abstractmethod
    async def get_detail_by_name(self, name: str) -> DetailItem | None:
        pass

    # -------------------------------
    # Accounting Period
    # -------------------------------
    @abstractmethod
    async def get_open_period(self) -> AccountingPeriod | None:
        pass

    # -------------------------------
    # Opening Equity
    # -------------------------------
    @abstractmethod
    async def get_opening_equity_account(self) -> DetailItem | None:
        pass

    @abstractmethod
    async def create_opening_equity_account(self) -> DetailItem:
        pass

    # -------------------------------
    # Auto Create
    # -------------------------------
    @abstractmethod
    async def auto_create_detail_item(
        self,
        data: DetailItemAutoCreateRequest
    ) -> DetailItem:
        pass
