from fastapi import Depends
from src.core.tenant_database import get_tenant_db
from src.repositories.commonjournal_repository import CommonJournalRepository
from src.repositories.accountingrule_repository import AccountingRuleRepository

from src.repositories.interfaces.iaccountingrule_repository import (
    IAccountingRuleRepository,
)
from src.services.commonjournal_service import CommonJournalService
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from sqlalchemy.ext.asyncio import AsyncSession


def get_common_journal_service(
    db: AsyncSession = Depends(get_tenant_db),
) -> ICommonJournalService:

    repo = CommonJournalRepository(db)
    rule_repo: IAccountingRuleRepository = AccountingRuleRepository(db)

    return CommonJournalService(
        repo,
        rule_repo,
    )
