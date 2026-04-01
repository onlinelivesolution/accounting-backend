from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from common.db.db import get_db
from src.services.commonjournal_service import CommonJournalService
from src.repositories.commonjournal_repository import CommonJournalRepository
from src.repositories.accountingrule_repository import AccountingRuleRepository
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.repositories.interfaces.iaccountingrule_repository import IAccountingRuleRepository

def get_common_journal_service(
    db: AsyncSession = Depends(get_db)
) -> ICommonJournalService:
    repo = CommonJournalRepository(db)
    rule_repo: IAccountingRuleRepository = AccountingRuleRepository(db)
    return CommonJournalService(repo, rule_repo)