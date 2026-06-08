from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# -------------------------------------------------
# IMPORT YOUR BASE MODEL METADATA
# -------------------------------------------------
from src.services.database import Base

# IMPORTANT: import all models so metadata is populated
import src.models  # noqa: F401
from src.models.accountingperiod import AccountingPeriod
from src.models.accountingrule  import AccountingRule
from src.models.accountingruledetail import AccountingRuleDetail
from src.models.accounttype import AccountType
from src.models.activitycenter import ActivityCenter
from src.models.advancesalary import AdvanceSalary
from src.models.bank_model import Bank
from src.models.bankaccount_model import BankAccount
from src.models.bankdeposit_model import BankDeposit
from src.models.bankwithdraw_model import BankWithdraw
from src.models.branch_model import Branch
from src.models.company import Company
from src.models.controlitem import ControlItem
from src.models.country_model import Country
from src.models.customers import Customer
from src.models.customerreceipt_model import CustomerReceipt
from src.models.customerreceiptsdetail_model import CustomerReceiptDetail
from src.models.detailitem import DetailItem
from src.models.employee import Employee
from src.models.employeehistory import EmployeeHistory
from src.models.employeeinvestment import EmployeeInvestment
from src.models.employeeloan import EmployeeLoan
from src.models.failedemployeeupload import FailedEmployeeUpload
from src.models.fatype import FAType
from src.models.employee import Employee

# -------------------------------------------------
# ALEMBIC CONFIG
# -------------------------------------------------
config = context.config

# Logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


# -------------------------------------------------
# GET DATABASE URL
# -------------------------------------------------
def get_database_url():
    """
    You can later replace this with:
    - tenant DB resolver
    - environment variable
    - master DB switch
    """
    return config.get_main_option("sqlalchemy.url")


# -------------------------------------------------
# OFFLINE MIGRATION
# -------------------------------------------------
def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # IMPORTANT: detect datatype changes
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------
# ONLINE MIGRATION
# -------------------------------------------------
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # detects datatype changes
            compare_server_default=True,  # detects default changes
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------
# RUN MODE
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
