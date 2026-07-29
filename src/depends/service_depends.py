from fastapi import Depends
from common.db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.systemadmin_service import SystemAdminService
from src.core.tenant_database import get_tenant_db
from src.repositories.period__repository import PeriodRepository
from src.services.period__service import PeriodService
from src.services.interfaces.idetailitem_service import IDetailItemService
from src.repositories.bankaccount_repository import BankAccountRepository
from src.repositories.detailitem_repository import DetailItemRepository

from src.depends.repository_depends import (
    get_login_repository,
    get_tenant_auth_repository,
)
from src.services.login_service import LoginService


def get_login_service(repository=Depends(get_login_repository)):

    return LoginService(repository)


from src.repositories.detailitem_repository import DetailItemRepository
from src.services.detailitem_service import DetailItemService
from src.services.interfaces.idetailitem_service import IDetailItemService


def get_detail_item_service(
    db: AsyncSession = Depends(get_tenant_db),
) -> IDetailItemService:

    repository = DetailItemRepository(db)
    return DetailItemService(repository, db)


from src.depends.repository_depends import get_vatrate_dropdown_repository
from src.repositories.interfaces.icommondropdown_repository import (
    ICommonDropdownRepository,
)
from src.services.interfaces.icommondropdown_service import ICommonDropdownService
from src.services.commondropdown_service import CommonDropdownService

from src.depends.repository_depends import get_reportingitem_repository
from src.repositories.interfaces.ireportingitem_repository import (
    IReportingItemRepository,
)
from src.services.interfaces.ireportingitem_service import IReportingItemService
from src.services.reportingitem_service import ReportingItemService

from src.depends.repository_depends import get_controlitem_repository
from src.repositories.interfaces.icontrolitem_repository import IControlItemRepository
from src.services.interfaces.icontrolitem_service import IControlItemService
from src.services.controlitem_service import ControlItemService

from src.depends.repository_depends import get_detailitem_repository
from src.repositories.interfaces.idetailitem_repository import IDetailItemRepository
from src.services.interfaces.idetailitem_service import IDetailItemService
from src.services.detailitem_service import DetailItemService

from src.depends.repository_depends import get_employee_repository
from src.repositories.interfaces.iemployee_repository import IEmployeeRepository
from src.services.interfaces.iemployee_service import IEmployeeService
from src.services.employee_service import EmployeeService

from src.depends.repository_depends import get_user_repository
from src.repositories.interfaces.iuser_repository import IUserRepository
from src.services.interfaces.iuser_service import IUserService
from src.services.user_service import UserService

from src.depends.repository_depends import get_role_permission_repository
from src.repositories.interfaces.irole_permission_repository import (
    IRolePermissionRepository,
)
from src.services.interfaces.irole_permission_service import IRolePermissionService
from src.services.role_permission_service import RolePermissionService

from src.depends.repository_depends import get_role_repository
from src.repositories.interfaces.irole_repository import IRoleRepository
from src.services.interfaces.irole_service import IRoleService
from src.services.role_service import RoleService

from src.depends.repository_depends import get_permission_repository
from src.repositories.interfaces.ipermission_repository import IPermissionRepository
from src.services.interfaces.ipermission_service import IPermissionService
from src.services.permission_service import PermissionService

from src.depends.repository_depends import get_assign_permission_repository
from src.repositories.interfaces.iassignpermission_repository import (
    IAssignPermissionRepository,
)
from src.services.interfaces.iassignpermission_service import IAssignPermissionService
from src.services.assignpermission_service import AssignPermissionService

from src.depends.repository_depends import get_login_repository
from src.repositories.interfaces.ilogin_repository import ILoginRepository
from src.services.interfaces.ilogin_service import ILoginService
from src.services.login_service import LoginService

from src.depends.repository_depends import (
    get_commonjournal_repository,
    get_accounting_rule_repository,
)
from src.repositories.interfaces.icommonjournal_repository import (
    ICommonJournalRepository,
)
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.repositories.interfaces.iaccountingrule_repository import (
    IAccountingRuleRepository,
)
from src.services.commonjournal_service import CommonJournalService


def get_commonjournal_service(
    repository: ICommonJournalRepository = Depends(get_commonjournal_repository),
    rule_repository: IAccountingRuleRepository = Depends(
        get_accounting_rule_repository
    ),
) -> ICommonJournalService:
    return CommonJournalService(repository, rule_repository)


from src.depends.repository_depends import get_accounting_rule_repository
from src.repositories.interfaces.iaccountingrule_repository import (
    IAccountingRuleRepository,
)
from src.services.interfaces.iaccountingrule_service import IAccountingRuleService
from src.services.accountingrule_service import AccountingRuleService


def get_accounting_rule_service(
    repository: IAccountingRuleRepository = Depends(get_accounting_rule_repository),
) -> IAccountingRuleService:
    return AccountingRuleService(repository)


from src.depends.repository_depends import get_tenant_repository
from src.repositories.interfaces.itenant_repository import ITenantRepository
from src.services.interfaces.itenant_service import ITenantService
from src.services.tenant_service import TenantService


def get_tenant_service(
    repository: ITenantRepository = Depends(get_tenant_repository),
) -> ITenantService:
    return TenantService(repository)


from src.depends.repository_depends import get_bank_deposit_repository
from src.repositories.interfaces.ibankdeposit_repository import IBankDepositRepository
from src.services.interfaces.ibankdeposit_service import IBankDepositService
from src.services.bankdeposit_service import BankDepositService

from src.depends.repository_depends import get_bank_withdraw_repository
from src.repositories.interfaces.ibankwithdraw_repository import IBankWithdrawRepository
from src.services.interfaces.ibankwithdraw_service import IBankWithdrawService
from src.services.bankwithdraw_service import BankWithdrawService

from src.depends.repository_depends import get_trial_balance_repository
from src.repositories.interfaces.itrialbalance__repository import (
    ITrialBalanceRepository,
)
from src.services.interfaces.itrialbalance__service import ITrialBalanceService
from src.services.trialbalance__service import TrialBalanceService

from src.depends.repository_depends import get_balance_sheet_repository
from src.repositories.interfaces.ibalancesheet__repository import (
    IBalanceSheetRepository,
)
from src.services.interfaces.ibalancesheet__service import IBalanceSheetService
from src.services.balancesheet__service import BalanceSheetService

from src.depends.repository_depends import get_period_repository
from src.repositories.interfaces.iperiod__repository import IPeriodRepository
from src.services.interfaces.iperiod__service import IPeriodService
from src.services.period__service import PeriodService

from src.repositories.detailitem_repository import DetailItemRepository

from src.depends.repository_depends import get_bank_account_repository
from src.repositories.interfaces.ibankaccount_repository import IBankAccountRepository
from src.services.interfaces.ibankaccount_service import IBankAccountService
from src.services.bankaccount_service import BankAccountService


def get_bank_account_service(
    db: AsyncSession = Depends(get_db),
    bank_repo: BankAccountRepository = Depends(get_bank_account_repository),
) -> IBankAccountService:

    # DetailItem service (needed to create ledger account)
    detailitem_repo = DetailItemRepository(db)
    detailitem_service = DetailItemService(detailitem_repo, db)

    return BankAccountService(
        bank_repo=bank_repo, detailitem_service=detailitem_service, db=db
    )

from src.depends.repository_depends import get_account_report_repository
from src.repositories.interfaces.iaccountreport__repository import (
    IAccountReportRepository,
)
from src.services.interfaces.iaccountreport__service import IAccountReportService
from src.services.accountreport__service import AccountReportService

def get_account_report_service(
    repository: IAccountReportRepository = Depends(get_account_report_repository),
) -> IAccountReportService:
    return AccountReportService(repository)


def get_db_period_service(
    db: AsyncSession = Depends(get_tenant_db),
):
    repo = PeriodRepository(db)
    return PeriodService(repo)


def get_period_service(
    repository: IPeriodRepository = Depends(get_period_repository),
) -> IPeriodService:
    return PeriodService(repository)


from src.depends.repository_depends import get_sales_order_repository
from src.repositories.interfaces.isalesorder_repository import ISalesOrderRepository
from src.services.interfaces.isalesorder_service import ISalesOrderService
from src.services.salesorder_service import SalesOrderService


def get_sales_order_service(
    repository: ISalesOrderRepository = Depends(get_sales_order_repository),
) -> ISalesOrderService:
    return SalesOrderService(repository)


from src.depends.repository_depends import get_payscalemappings_repository
from src.repositories.interfaces.ipayscalemappings_repository import (
    IPayScaleMappingRepository,
)
from src.services.interfaces.ipayscalemappings_service import IPayScaleMappingService
from src.services.payscalemappings_service import PayScaleMappingService


def get_payscalemapping_service(
    repository: IPayScaleMappingRepository = Depends(get_payscalemappings_repository),
) -> IPayScaleMappingService:
    return PayScaleMappingService(repository)


from src.depends.repository_depends import get_generatesalary_repository
from src.repositories.interfaces.igeneratesalary_repository import (
    IGenerateSalaryRepository,
)
from src.services.interfaces.igeneratesalary_service import IGenerateSalaryService
from src.services.generatesalary_service import GenerateSalaryService


def get_generatesalary_service(
    repository: IGenerateSalaryRepository = Depends(get_generatesalary_repository),
) -> IGenerateSalaryService:
    return GenerateSalaryService(repository)


from src.depends.repository_depends import get_salarydetail_repository
from src.repositories.interfaces.isalarydetail_repository import ISalaryDetailRepository
from src.services.interfaces.isalarydetail_service import ISalaryDetailService
from src.services.salarydetail_service import SalaryDetailService


def get_salarydetail_service(
    repository: ISalaryDetailRepository = Depends(get_salarydetail_repository),
) -> ISalaryDetailService:
    return SalaryDetailService(repository)


from src.depends.repository_depends import get_quotation_repository
from src.repositories.interfaces.iquotation_repository import IQuotationRepository
from src.services.interfaces.iquotation_service import IQuotationService
from src.services.quotation_service import QuotationService


def get_quotation_service(
    repository: IQuotationRepository = Depends(get_quotation_repository),
) -> IQuotationService:
    return QuotationService(repository)


from src.depends.repository_depends import get_systemadmin_repository
from src.repositories.interfaces.isystemadmin_repository import ISystemAdminRepository
from src.services.interfaces.isystemadmin_service import ISystemAdminService
from src.services.systemadmin_service import SystemAdminService


def get_systemadmin_service(
    repository: ISystemAdminRepository = Depends(get_systemadmin_repository),
) -> ISystemAdminService:
    return SystemAdminService(repository)


from src.depends.repository_depends import get_manage_tenant_repository
from src.repositories.interfaces.imanagetenant_repository import IManageTenantRepository
from src.services.interfaces.imanagetenant_service import IManageTenantService
from src.services.managetenant_service import ManageTenantService


def get_manage_tenant_service(
    repository: IManageTenantRepository = Depends(get_manage_tenant_repository),
) -> IManageTenantService:
    return ManageTenantService(repository)


def get_systemadmin_service(
    repository: ISystemAdminRepository = Depends(get_systemadmin_repository),
) -> ISystemAdminService:
    return SystemAdminService(repository)


from src.depends.repository_depends import get_customer_receipt_repository
from src.repositories.interfaces.icustomerreceipt_repository import (
    ICustomerReceiptRepository,
)
from src.services.interfaces.icustomerreceipt_service import ICustomerReceiptService
from src.services.customerreceipt_service import CustomerReceiptService
from src.depends.common_service_depends import get_common_journal_service


def get_customer_receipt_service(
    repository: ICustomerReceiptRepository = Depends(get_customer_receipt_repository),
    common_journal_service: ICommonJournalService = Depends(
        get_common_journal_service
    ),  # ✅ ADD
) -> ICustomerReceiptService:
    return CustomerReceiptService(repository, common_journal_service)


from src.depends.repository_depends import get_sales_invoice_repository
from src.repositories.interfaces.isalesinvoice_repository import ISalesInvoiceRepository
from src.services.interfaces.isalesinvoice_service import ISalesInvoiceService
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.depends.common_service_depends import get_common_journal_service
from src.services.salesinvoice_service import SalesInvoiceService

from src.services.common.interfaces.iemail_service import IEmailService
from src.services.common.interfaces.ipdf_service import IPdfService
from src.repositories.interfaces.iemail_repository import IEmailRepository
from src.repositories.interfaces.ipdf_repository import IPdfRepository

from src.depends.repository_depends import get_email_repository

from src.depends.repository_depends import get_pdf_repository


def get_sales_invoice_service(
    repository: ISalesInvoiceRepository = Depends(get_sales_invoice_repository),
    journal_service: ICommonJournalService = Depends(get_common_journal_service),
    email_repository: IEmailRepository = Depends(get_email_repository),
    pdf_repository: IPdfRepository = Depends(get_pdf_repository),
) -> ISalesInvoiceService:

    return SalesInvoiceService(
        repository, journal_service, email_repository, pdf_repository
    )


from src.depends.repository_depends import get_salarypayment_repository
from src.repositories.interfaces.isalarypayment_repository import (
    ISalaryPaymentRepository,
)
from src.services.interfaces.isalarypayment_service import ISalaryPaymentService
from src.services.salarypayment_service import SalaryPaymentService


def get_salarypayment_service(
    repository: ISalaryPaymentRepository = Depends(get_salarypayment_repository),
    journal_service: ICommonJournalService = Depends(get_common_journal_service),
) -> ISalaryPaymentService:
    return SalaryPaymentService(repository, journal_service)


from src.depends.repository_depends import get_bank_transaction_repository
from src.repositories.interfaces.ibanktransaction_repository import (
    IBankTransactionRepository,
)
from src.services.interfaces.ibanktransaction_service import IBankTransactionService
from src.services.banktransaction_service import BankTransactionService


def get_bank_transaction_service(
    repository: IBankTransactionRepository = Depends(get_bank_transaction_repository),
    db: AsyncSession = Depends(get_db),
) -> IBankTransactionService:
    return BankTransactionService(repository, db)


from src.depends.repository_depends import get_common_repository
from src.repositories.interfaces.icommon_repository import ICommonRepository
from src.services.interfaces.icommon_service import ICommonService
from src.services.common_service import CommonService


def get_common_service(
    repository: ICommonRepository = Depends(get_common_repository),
) -> ICommonService:
    return CommonService(repository)


def get_balance_sheet_service(
    repository: IBalanceSheetRepository = Depends(get_balance_sheet_repository),
) -> IBalanceSheetService:
    return BalanceSheetService(repository)


def get_trial_balance_service(
    repository: ITrialBalanceRepository = Depends(get_trial_balance_repository),
) -> ITrialBalanceService:
    return TrialBalanceService(repository)


def get_bank_withdraw_service(
    repository: IBankWithdrawRepository = Depends(get_bank_withdraw_repository),
) -> IBankWithdrawService:
    return BankWithdrawService(repository)


def get_bank_deposit_service(
    repository: IBankDepositRepository = Depends(get_bank_deposit_repository),
) -> IBankDepositService:
    return BankDepositService(repository)


def get_assign_permission_service(
    repository: IAssignPermissionRepository = Depends(get_assign_permission_repository),
) -> IAssignPermissionService:
    return AssignPermissionService(repository)


def get_login_service(
    repository: ILoginRepository = Depends(get_login_repository),
) -> ILoginService:
    return LoginService(repository)


def get_role_service(
    repository: IRoleRepository = Depends(get_role_repository),
) -> IRoleService:
    return RoleService(repository)


def get_permission_service(
    repository: IPermissionRepository = Depends(get_permission_repository),
) -> IPermissionService:
    return PermissionService(repository)


def get_role_permission_service(
    repository: IRolePermissionRepository = Depends(get_role_permission_repository),
) -> IRolePermissionService:
    return RolePermissionService(repository)


def get_user_service(
    repository: IUserRepository = Depends(get_user_repository),
) -> IUserService:
    return UserService(repository)


def get_employee_service(
    repository: IEmployeeRepository = Depends(get_employee_repository),
) -> IEmployeeService:
    return EmployeeService(repository)


def get_controlitem_service(
    repository: IControlItemRepository = Depends(get_controlitem_repository),
) -> IControlItemService:
    return ControlItemService(repository)


def get_reportingitem_service(
    repository: IReportingItemRepository = Depends(get_reportingitem_repository),
) -> IReportingItemService:
    return ReportingItemService(repository)


def get_detailitem_service(
    repository: IDetailItemRepository = Depends(get_detailitem_repository),
) -> IDetailItemService:
    return DetailItemService(repository)


def get_common_dropdown_service(
    repository: ICommonDropdownRepository = Depends(get_vatrate_dropdown_repository),
) -> ICommonDropdownService:
    return CommonDropdownService(repository)


from src.services.tenantauth_service import TenantAuthService
from src.services.interfaces.itenantauth_service import ITenantAuthService
from src.repositories.interfaces.itenantauth_repository import ITenantAuthRepository


def get_tenant_auth_service(
    repository: ITenantAuthRepository = Depends(get_tenant_auth_repository),
) -> ITenantAuthService:

    return TenantAuthService(repository)
