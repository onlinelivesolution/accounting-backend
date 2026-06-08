from sqlalchemy import select, text
from datetime import datetime
from src.services.database import AsyncSessionLocal
from src.core.tenant_database import get_tenant_session

# MODELS

from src.models.company import Company
from src.models.role_model import Role
from src.models.permission_model import Permission
from src.models.permission_action_model import PermissionAction
from src.models.role_permission_action_model import (
    RolePermissionAction,
)
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem

# USER MODEL
from src.models.user_model import UserInfo

# PASSWORD HASHER
from common.utils.security import hash_password

# ====================================
# DEFAULT PASSWORD
# ====================================


def generate_default_password():

    return "Admin@123"


# ====================================
# CREATE ADMIN USER
# ====================================


async def create_admin_user(tenant_db, email: str):

    # Generate Password
    password = generate_default_password()

    # Safe string
    password = str(password).strip()

    print("===================================")
    print("GENERATED PASSWORD:", password)
    print("PASSWORD LENGTH:", len(password))
    print("===================================")

    # HASH PASSWORD
    hashed_password = hash_password(password)

    print("HASH GENERATED SUCCESSFULLY")

    # CHECK EXISTING USER
    existing_user_result = await tenant_db.execute(
        select(UserInfo).where(UserInfo.userName == email)
    )

    existing_user = existing_user_result.scalars().first()

    # SKIP IF EXISTS
    if existing_user:

        print("ADMIN USER ALREADY EXISTS")

        return

    # CREATE USER
    admin_user = UserInfo(
        userName=email,
        fullName="Admin User",
        email=email,
        passwordHash=hashed_password,
        roleID=1,
        isActive=True,
        isSuperAdmin=True,
        createdBy='superadmin',
        createdDate=datetime.utcnow(),
    )

    tenant_db.add(admin_user)

    await tenant_db.commit()

    print("===================================")
    print("ADMIN USER CREATED SUCCESSFULLY")
    print("LOGIN EMAIL:", email)
    print("TEMP PASSWORD:", password)
    print("===================================")


# ====================================
# COPY MASTER DATA
# ====================================


async def copy_master_data(database_name: str, email: str):

    # MASTER DB SESSION
    async with AsyncSessionLocal() as master_db:

        # TENANT DB SESSION
        tenant_db = get_tenant_session(database_name)

        try:

            # ====================================
            # RESET OLD DATA
            # CHILD → PARENT
            # ====================================

            await tenant_db.execute(text("DELETE FROM DetailItem"))

            await tenant_db.execute(text("DELETE FROM ReportingItem"))

            await tenant_db.execute(text("DELETE FROM ControlItem"))

            await tenant_db.execute(text("DELETE FROM RolePermissionAction"))

            await tenant_db.execute(text("DELETE FROM PermissionAction"))

            await tenant_db.execute(text("DELETE FROM Permission"))

            await tenant_db.execute(text("DELETE FROM Role"))

            await tenant_db.execute(text("DELETE FROM Company"))

            await tenant_db.commit()

            print("OLD SEED DATA DELETED")

            # ====================================
            # COPY COMPANY
            # ====================================

            company_result = await master_db.execute(select(Company))

            companies = company_result.scalars().all()

            tenant_db.add_all(
                [
                    Company(
                        companyCode=i.companyCode,
                        companyName=i.companyName,
                    )
                    for i in companies
                ]
            )

            await tenant_db.commit()

            print("Company Inserted:", len(companies))

            # ====================================
            # COPY ROLE
            # ====================================

            role_result = await master_db.execute(select(Role))

            roles = role_result.scalars().all()

            tenant_db.add_all(
                [
                    Role(
                        roleID=i.roleID,
                        roleName=i.roleName,
                        description=i.description,
                        isActive=i.isActive,
                        companyCode=i.companyCode,
                        createdBy=i.createdBy,
                        createdDate=i.createdDate,
                        updatedBy=i.updatedBy,
                        updatedDate=i.updatedDate,
                    )
                    for i in roles
                ]
            )

            await tenant_db.commit()

            print("Role Inserted:", len(roles))

            # ====================================
            # COPY PERMISSION
            # ====================================

            permission_result = await master_db.execute(select(Permission))

            permissions = permission_result.scalars().all()

            tenant_db.add_all(
                [
                    Permission(
                        permissionID=i.permissionID,
                        permissionName=i.permissionName,
                        moduleName=i.moduleName,
                        description=i.description,
                        createdBy=i.createdBy,
                        createdDate=i.createdDate,
                        updatedBy=i.updatedBy,
                        updatedDate=i.updatedDate,
                        isActive=i.isActive,
                        companyCode=i.companyCode,
                        permissionKey=i.permissionKey,
                    )
                    for i in permissions
                ]
            )

            await tenant_db.commit()

            print("Permission Inserted:", len(permissions))

            # ====================================
            # COPY PERMISSION ACTION
            # ====================================

            permission_action_result = await master_db.execute(select(PermissionAction))

            permission_actions = permission_action_result.scalars().all()

            tenant_db.add_all(
                [
                    PermissionAction(
                        permissionActionID=i.permissionActionID,
                        actionName=i.actionName,
                        actionKey=i.actionKey,
                        isActive=i.isActive,
                        createdBy=i.createdBy,
                        createdDate=i.createdDate,
                        updatedBy=i.updatedBy,
                        updatedDate=i.updatedDate,
                    )
                    for i in permission_actions
                ]
            )

            await tenant_db.commit()

            print("PermissionAction Inserted:", len(permission_actions))

            # ====================================
            # COPY ROLE PERMISSION ACTION
            # ====================================

            role_permission_action_result = await master_db.execute(
                select(RolePermissionAction)
            )

            role_permission_actions = role_permission_action_result.scalars().all()

            tenant_db.add_all(
                [
                    RolePermissionAction(
                        rolePermissionActionID=i.rolePermissionActionID,
                        roleID=i.roleID,
                        permissionID=i.permissionID,
                        permissionActionID=i.permissionActionID,
                        isAllowed=i.isAllowed,
                        createdBy=i.createdBy,
                        createdDate=i.createdDate,
                        updatedBy=i.updatedBy,
                        updatedDate=i.updatedDate,
                    )
                    for i in role_permission_actions
                ]
            )

            await tenant_db.commit()

            print(
                "RolePermissionAction Inserted:",
                len(role_permission_actions),
            )

            # ====================================
            # COPY CONTROL ITEM
            # ====================================

            control_item_result = await master_db.execute(select(ControlItem))

            control_items = control_item_result.scalars().all()

            tenant_db.add_all(
                [
                    ControlItem(
                        controlItemCode=i.controlItemCode,
                        controlItemName=i.controlItemName,
                        accountCategory=i.accountCategory,
                        financialStatementType=i.financialStatementType,
                        isActive=i.isActive,
                    )
                    for i in control_items
                ]
            )

            await tenant_db.commit()

            print("ControlItem Inserted:", len(control_items))

            # ====================================
            # COPY REPORTING ITEM
            # ====================================

            reporting_item_result = await master_db.execute(select(ReportingItem))

            reporting_items = reporting_item_result.scalars().all()

            tenant_db.add_all(
                [
                    ReportingItem(
                        reportingItemCode=i.reportingItemCode,
                        reportingItemName=i.reportingItemName,
                        controlItemCode=i.controlItemCode,
                    )
                    for i in reporting_items
                ]
            )

            await tenant_db.commit()

            print("ReportingItem Inserted:", len(reporting_items))

            # ====================================
            # COPY DETAIL ITEM
            # ====================================

            detail_item_result = await master_db.execute(select(DetailItem))

            detail_items = detail_item_result.scalars().all()

            tenant_db.add_all(
                [
                    DetailItem(
                        detailItemCode=i.detailItemCode,
                        detailItemName=i.detailItemName,
                        reportingItemCode=i.reportingItemCode,
                        normalBalance=i.normalBalance,
                        isActive=i.isActive,
                        loadType=i.loadType,
                    )
                    for i in detail_items
                ]
            )

            await tenant_db.commit()

            print("DetailItem Inserted:", len(detail_items))

            # ====================================
            # VERIFY COUNTS
            # ====================================

            control_count_result = await tenant_db.execute(select(ControlItem))

            reporting_count_result = await tenant_db.execute(select(ReportingItem))

            detail_count_result = await tenant_db.execute(select(DetailItem))

            print(
                "Tenant ControlItem Count:", len(control_count_result.scalars().all())
            )

            print(
                "Tenant ReportingItem Count:",
                len(reporting_count_result.scalars().all()),
            )

            print("Tenant DetailItem Count:", len(detail_count_result.scalars().all()))

            # ====================================
            # CREATE ADMIN USER
            # ====================================

            await create_admin_user(tenant_db, email)

            print("TENANT SETUP COMPLETED")

        except Exception as e:

            await tenant_db.rollback()

            print("===================================")
            print("SEED ERROR:", str(e))
            print("===================================")

            raise e

        finally:

            await tenant_db.close()
