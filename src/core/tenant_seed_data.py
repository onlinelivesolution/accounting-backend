from sqlalchemy import select

from src.services.database import AsyncSessionLocal

from src.core.tenant_database import get_tenant_session

# IMPORT MODELS

from src.models.company import Company
from src.models.role_model import Role
from src.models.permission_model import Permission
from src.models.permission_action_model import PermissionAction
from src.models.role_permission_action_model import RolePermissionAction
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem


async def copy_master_data(database_name: str):

    # MASTER DB SESSION
    async with AsyncSessionLocal() as master_db:

        # TENANT DB SESSION
        tenant_db = get_tenant_session(database_name)

        try:

            # =========================
            # COPY COMPANY
            # =========================

            company_result = await master_db.execute(select(Company))

            companies = company_result.scalars().all()

            for company in companies:

                tenant_company = Company(
                    companyCode=company.companyCode,
                    companyName=company.companyName,
                )

                tenant_db.add(tenant_company)

            await tenant_db.commit()

            # =========================
            # COPY ROLE
            # =========================

            role_result = await master_db.execute(select(Role))

            roles = role_result.scalars().all()

            for role in roles:

                tenant_role = Role(
                    roleID=role.roleID,
                    roleName=role.roleName,
                    description=role.description,
                    isActive=role.isActive,
                    companyCode=role.companyCode,
                    createdBy=role.createdBy,
                    createdDate=role.createdDate,
                    updatedBy=role.updatedBy,
                    updatedDate=role.updatedDate,
                )

                tenant_db.add(tenant_role)

            await tenant_db.commit()

            # =========================
            # COPY PERMISSION
            # =========================

            permission_result = await master_db.execute(select(Permission))

            permissions = permission_result.scalars().all()

            for permission in permissions:

                tenant_permission = Permission(
                    permissionID=permission.permissionID,
                    permissionName=permission.permissionName,
                    moduleName=permission.moduleName,
                    description=permission.description,
                    createdBy=permission.createdBy,
                    createdDate=permission.createdDate,
                    updatedBy=permission.updatedBy,
                    updatedDate=permission.updatedDate,
                    isActive=permission.isActive,
                    companyCode=permission.companyCode,
                    permissionKey=permission.permissionKey,
                )

                tenant_db.add(tenant_permission)

            await tenant_db.commit()

            # =========================
            # COPY PERMISSION ACTION
            # =========================

            permission_action_result = await master_db.execute(select(PermissionAction))

            permission_actions = permission_action_result.scalars().all()

            for permission_action in permission_actions:

                tenant_permission_action = PermissionAction(
                    permissionActionID=permission_action.permissionActionID,
                    actionName=permission_action.actionName,
                    actionKey=permission_action.actionKey,
                    isActive=permission_action.isActive,
                    createdBy=permission_action.createdBy,
                    createdDate=permission_action.createdDate,
                    updatedBy=permission_action.updatedBy,
                    updatedDate=permission_action.updatedDate,
                )

                tenant_db.add(tenant_permission_action)

            await tenant_db.commit()

            # =========================
            # COPY ROLE PERMISSION ACTION
            # =========================

            role_permission_action_result = await master_db.execute(
                select(RolePermissionAction)
            )

            role_permission_actions = role_permission_action_result.scalars().all()

            for role_permission_action in role_permission_actions:

                tenant_role_permission_action = RolePermissionAction(
                    rolePermissionActionID=role_permission_action.rolePermissionActionID,
                    roleID=role_permission_action.roleID,
                    permissionID=role_permission_action.permissionID,
                    permissionActionID=role_permission_action.permissionActionID,
                    isAllowed=role_permission_action.isAllowed,
                    createdBy=role_permission_action.createdBy,
                    createdDate=role_permission_action.createdDate,
                    updatedBy=role_permission_action.updatedBy,
                    updatedDate=role_permission_action.updatedDate,
                )

                tenant_db.add(tenant_role_permission_action)

            await tenant_db.commit()

            # =========================
            # COPY CONTROL ITEM
            # =========================

            control_item_result = await master_db.execute(select(ControlItem))

            control_items = control_item_result.scalars().all()

            tenant_db.add_all([
                ControlItem(
                    controlItemCode=i.controlItemCode,
                    controlItemName=i.controlItemName,
                    accountCategory=i.accountCategory,
                    financialStatementType=i.financialStatementType,
                    isActive=i.isActive,
                )
                for i in control_items
            ])

            await tenant_db.commit()
            tenant_db.expunge_all()

            # =========================
            # COPY REPORTING ITEM
            # =========================

            reporting_item_result = await master_db.execute(select(ReportingItem))

            reporting_items = reporting_item_result.scalars().all()

            tenant_db.add_all([
                ReportingItem(
                    reportingItemCode=i.reportingItemCode,
                    reportingItemName=i.reportingItemName,
                    controlItemCode=i.controlItemCode,
                )
                for i in reporting_items
            ])

            await tenant_db.commit()
            tenant_db.expunge_all()

            # =========================
            # DEBUG REPORTING ITEMS
            # =========================

            check_result = await tenant_db.execute(select(ReportingItem))

            inserted_reporting_items = check_result.scalars().all()

            print(
                "Reporting Items Count:",
                len(inserted_reporting_items),
            )

            # =========================
            # COPY DETAIL ITEM
            # =========================

            detail_item_result = await master_db.execute(select(DetailItem))

            detail_items = detail_item_result.scalars().all()

            tenant_db.add_all([
                DetailItem(
                    detailItemCode=i.detailItemCode,
                    detailItemName=i.detailItemName,
                    reportingItemCode=i.reportingItemCode,
                    normalBalance=i.normalBalance,
                    isActive=i.isActive,
                    loadType=i.loadType,
                )
                for i in detail_items
            ])

            await tenant_db.commit()
            tenant_db.expunge_all()

            print("Master data copied successfully")

        except Exception as e:

            await tenant_db.rollback()

            print("Seed Data Error:", str(e))

            raise e

        finally:

            await tenant_db.close()
