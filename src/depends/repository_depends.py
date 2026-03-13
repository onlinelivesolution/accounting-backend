from fastapi import Depends
from common.db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.interfaces.icommon_repository import ICommonRepository
from src.repositories.common_repository import CommonRepository

from src.repositories.interfaces.icommondropdown_repository import ICommonDropdownRepository
from src.repositories.commondropdown_repository import CommonDropdownRepository

from src.repositories.interfaces.ireportingitem_repository import IReportingItemRepository
from src.repositories.reportingitem_repository import ReportingItemRepository

from src.repositories.interfaces.idetailitem_repository import IDetailItemRepository
from src.repositories.detailitem_repository import DetailItemRepository

from src.repositories.interfaces.icontrolitem_repository import IControlItemRepository
from src.repositories.controlitem_repository import ControlItemRepository
from src.repositories.interfaces.igeneratesalary_repository import IGenerateSalaryRepository

from src.repositories.interfaces.isalarydetail_repository import ISalaryDetailRepository
from src.repositories.salarydetail_repository import SalaryDetailRepository

from src.repositories.generatesalary_repository import GenerateSalaryRepository

from src.repositories.interfaces.ipayscalemappings_repository import IPayScaleMappingRepository
from src.repositories.payscalemappings_repository import PayScaleMappingRepository

from src.repositories.interfaces.iemployee_repository import IEmployeeRepository
from src.repositories.employee_repository import EmployeeRepository

from src.repositories.interfaces.iuser_repository import IUserRepository
from src.repositories.user_repository import UserRepository

from src.repositories.interfaces.irole_permission_repository import IRolePermissionRepository
from src.repositories.role_permission_repository import RolePermissionRepository

from src.repositories.interfaces.irole_repository import IRoleRepository
from src.repositories.role_repository import RoleRepository

from src.repositories.interfaces.ipermission_repository import IPermissionRepository
from src.repositories.permission_repository import PermissionRepository

from src.repositories.interfaces.iassignpermission_repository import IAssignPermissionRepository
from src.repositories.assignpermission_repository import AssignPermissionRepository

from src.repositories.interfaces.ilogin_repository import ILoginRepository
from src.repositories.login_repository import LoginRepository

from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
from src.repositories.commonjournal_repository import CommonJournalRepository

from src.repositories.interfaces.ibankaccount_repository import IBankAccountRepository
from src.repositories.bankaccount_repository import BankAccountRepository

from src.repositories.interfaces.ibankdeposit_repository import IBankDepositRepository
from src.repositories.bankdeposit_repository import BankDepositRepository

from src.repositories.interfaces.ibankwithdraw_repository import IBankWithdrawRepository
from src.repositories.bankwithdraw_repository import BankWithdrawRepository

from src.repositories.interfaces.itrialbalance__repository import ITrialBalanceRepository
from src.repositories.trialbalance__repository import TrialBalanceRepository

from src.repositories.interfaces.ibalancesheet__repository import IBalanceSheetRepository
from src.repositories.balancesheet__repository import BalanceSheetRepository

from src.repositories.interfaces.iperiod__repository import IPeriodRepository
from src.repositories.period__repository import PeriodRepository

from src.repositories.interfaces.iaccountreport__repository import IAccountReportRepository
from src.repositories.accountreport__repository import AccountReportRepository

from src.repositories.interfaces.ibanktransaction_repository import IBankTransactionRepository
from src.repositories.banktransaction_repository import BankTransactionRepository

def get_vatrate_dropdown_repository(db: AsyncSession = Depends(get_db))->ICommonDropdownRepository:
    return CommonDropdownRepository(db)


from src.repositories.interfaces.iquotation_repository import IQuotationRepository
from src.repositories.quotation_repository import QuotationRepository

def get_quotation_repository(db: AsyncSession = Depends(get_db))->IQuotationRepository:
    return QuotationRepository(db)

from src.repositories.interfaces.isalesinvoice_repository import ISalesInvoiceRepository
from src.repositories.salesinvoice_repository import SalesInvoiceRepository

def get_sales_invoice_repository(db: AsyncSession = Depends(get_db))->ISalesInvoiceRepository:
    return SalesInvoiceRepository(db)

from src.repositories.interfaces.iaccountingrule_repository import IAccountingRuleRepository
from src.repositories.accountingrule_repository import AccountingRuleRepository

def get_accounting_rule_repository(db: AsyncSession = Depends(get_db))->IAccountingRuleRepository:
    return AccountingRuleRepository(db)


from src.repositories.interfaces.isalesorder_repository import ISalesOrderRepository
from src.repositories.salesorder_repository import SalesOrderRepository

def get_sales_order_repository(db: AsyncSession = Depends(get_db))->ISalesOrderRepository:
    return SalesOrderRepository(db)


def get_bank_transaction_repository(db: AsyncSession = Depends(get_db))->IBankTransactionRepository:
    return BankTransactionRepository(db)

def get_account_report_repository(db: AsyncSession = Depends(get_db))->IAccountReportRepository:
    return AccountReportRepository(db)

def get_period_repository(db: AsyncSession = Depends(get_db))->IPeriodRepository:
    return PeriodRepository(db)

def get_balance_sheet_repository(db: AsyncSession = Depends(get_db))->IBalanceSheetRepository:
    return BalanceSheetRepository(db)

def get_trial_balance_repository(db: AsyncSession = Depends(get_db))->ITrialBalanceRepository:
    return TrialBalanceRepository(db)

def get_bank_withdraw_repository(db: AsyncSession = Depends(get_db))->IBankWithdrawRepository:
    return BankWithdrawRepository(db)

def get_bank_deposit_repository(db: AsyncSession = Depends(get_db))->IBankDepositRepository:
    return BankDepositRepository(db)

def get_bank_account_repository(db: AsyncSession = Depends(get_db)) -> IBankAccountRepository:
    return BankAccountRepository(db)

def get_commonjournal_repository(db: AsyncSession = Depends(get_db))->ICommonJournalRepository:
    return CommonJournalRepository(db)

def get_common_repository(db: AsyncSession = Depends(get_db))->ICommonRepository:
    return CommonRepository(db)

def get_login_repository(db: AsyncSession = Depends(get_db))->ILoginRepository:
    return LoginRepository(db)

def get_assign_permission_repository(db: AsyncSession = Depends(get_db))->IAssignPermissionRepository:
    return AssignPermissionRepository(db)

def get_role_repository(db: AsyncSession = Depends(get_db))->IRoleRepository:
    return RoleRepository(db)

def get_permission_repository(db: AsyncSession = Depends(get_db))->IPermissionRepository:
    return PermissionRepository(db)

def get_role_permission_repository(db: AsyncSession = Depends(get_db))->IRolePermissionRepository:
    return RolePermissionRepository(db)

def get_user_repository(db: AsyncSession = Depends(get_db))->IUserRepository:
    return UserRepository(db)

def get_employee_repository(db: AsyncSession = Depends(get_db))->IEmployeeRepository:
    return EmployeeRepository(db)

def get_controlitem_repository(db: AsyncSession = Depends(get_db))->IControlItemRepository:
    return ControlItemRepository(db)

def get_reportingitem_repository(db: AsyncSession = Depends(get_db))->IReportingItemRepository:
    return ReportingItemRepository(db)

def get_detailitem_repository(db: AsyncSession = Depends(get_db))->IDetailItemRepository:
    return DetailItemRepository(db)

def get_payscalemapping_repository(db: AsyncSession = Depends(get_db))->IPayScaleMappingRepository:
    return PayScaleMappingRepository(db)

def get_generatesalary_repository(db: AsyncSession = Depends(get_db))->IGenerateSalaryRepository:
    return GenerateSalaryRepository(db)

def get_salarydetail_repository(db: AsyncSession = Depends(get_db))->ISalaryDetailRepository:
    return SalaryDetailRepository(db)