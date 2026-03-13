from pydantic import BaseModel
from typing import List


class AccountingRuleDetailRequest(BaseModel):
    accountCode: str
    entryType: str
    amountSource: str


class AccountingRuleCreateRequest(BaseModel):
    ruleCode: str
    moduleName: str
    description: str
    details: List[AccountingRuleDetailRequest]