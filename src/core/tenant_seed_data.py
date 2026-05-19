from sqlalchemy import select

from src.services.database import AsyncSessionLocal

from src.core.tenant_database import get_tenant_session

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
                    companyCode=company.companyCode, companyName=company.companyName
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
            # COPY Permission
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
            # COPY PermissionAction
            # =========================

            permissionAction_result = await master_db.execute(select(PermissionAction))

            permissionActions = permissionAction_result.scalars().all()

            for permissionAction in permissionActions:

                tenant_permissionAction = PermissionAction(
                    permissionActionID=permissionAction.permissionActionID,
                    actionName=permissionAction.actionName,
                    actionKey=permissionAction.actionKey,
                    isActive=permissionAction.isActive,
                    createdBy=permissionAction.createdBy,
                    createdDate=permissionAction.createdDate,
                    updatedBy=permissionAction.updatedBy,
                    updatedDate=permissionAction.updatedDate,
                )

                tenant_db.add(tenant_permissionAction)

                await tenant_db.commit()
            # =========================
            # COPY RolePermissionAction
            # =========================

            roleermissionAction_result = await master_db.execute(
                select(RolePermissionAction)
            )

            rolePermissionActions = roleermissionAction_result.scalars().all()

            for rolePermissionAction in rolePermissionActions:

                tenant_rolePermissionAction = RolePermissionAction(
                    rolePermissionActionID=rolePermissionAction.rolePermissionActionID,
                    roleID=rolePermissionAction.roleID,
                    permissionID=rolePermissionAction.permissionID,
                    permissionActionID=rolePermissionAction.permissionActionID,
                    isAllowed=rolePermissionAction.isAllowed,
                    createdBy=rolePermissionAction.createdBy,
                    createdDate=rolePermissionAction.createdDate,
                    updatedBy=rolePermissionAction.updatedBy,
                    updatedDate=rolePermissionAction.updatedDate,
                )

                tenant_db.add(tenant_rolePermissionAction)

                await tenant_db.commit()

            # =========================
            # Copy ControlItem
            # =========================

            controlItem_result = await master_db.execute(select(ControlItem))

            controlItems = controlItem_result.scalars().all()

            for controlItem in controlItems:

                tenant_controlItem = ControlItem(
                    controlItemCode=controlItem.controlItemCode,
                    controlItemName=controlItem.controlItemName,
                    accountCategory=controlItem.accountCategory,
                    financialStatementType=controlItem.financialStatementType,
                    isActive=controlItem.isActive,
                )

            tenant_db.add(tenant_controlItem)

            await tenant_db.commit()

            # =========================
            # Copy ReportingItem
            # =========================

            reportingItem_result = await master_db.execute(select(ReportingItem))

            reportingItems = reportingItem_result.scalars().all()

            for reportingItem in reportingItems:

                tenant_reportingItem = ReportingItem(
                    reportingItemCode=reportingItem.reportingItemCode,
                    reportingItemName=reportingItem.reportingItemName,
                    controlItemCode=reportingItem.controlItemCode,
                )

            tenant_db.add(tenant_reportingItem)

            await tenant_db.commit()

            # =========================
            # Copy DetailItem
            # =========================

            detailItem_result = await master_db.execute(select(DetailItem))

            detailItems = detailItem_result.scalars().all()

            for detailItem in detailItems:

                tenant_detailItem = DetailItem(
                    detailItemCode=detailItem.detailItemCode,
                    detailItemName=detailItem.detailItemName,
                    reportingItemCode=detailItem.reportingItemCode,
                    normalBalance=detailItem.normalBalance,
                    isActive=detailItem.isActive,
                    loadType=detailItem.loadType,
                )

            tenant_db.add(tenant_detailItem)

            await tenant_db.commit()

        except Exception as e:

            await tenant_db.rollback()

            raise e

        finally:

            await tenant_db.close()
