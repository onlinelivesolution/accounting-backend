from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class AccountingRuleDetailRequest(BaseModel):

    accountCode: str
    entryType: str
    amountSource: str


class AccountingRuleRequest(BaseModel):

    ruleCode: str
    moduleName: str
    description: str
    details: List[AccountingRuleDetailRequest]