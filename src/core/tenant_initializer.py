from src.core.tenant_seed_data import copy_master_data
from src.core.tenant_accounting_period import create_default_accounting_period
from src.core.tenant_fiscal_year import create_default_fiscal_year


async def initialize_new_tenant(
    database_name: str,
    tenant,
):
    """
    Initialize all default data for a newly approved tenant.
    """

    # Copy master data + create tenant admin
    await copy_master_data(
        database_name,
        tenant.email,
        tenant.passwordHash,
    )

    # Create default Accounting Period
    await create_default_accounting_period(database_name)
    
    # Create default Fiscal Year
    await create_default_fiscal_year(database_name)

    # Future initialization

    # await create_default_financial_year(database_name)
    # await create_default_number_sequences(database_name)
    # await create_default_settings(database_name)
    # await create_default_dashboard(database_name)
