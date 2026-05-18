# main.py
from fastapi import FastAPI # or whatever your endpoint file 
from src.routers import customerreceipt_router
from src.routers import tenant_router
from src.routers import salesinvoice_router
from src.routers import quotation_router
from src.routers import accountingrule_router
from src.routers import salesorder_router
from src.routers import commondropdown_router
from src.routers import banktransaction_router
from src.routers import accountreport__router
from src.routers import period__router
from src.routers import closing_router
from src.routers import balancesheet_router
from src.routers import trialbalance_router
from src.routers import bankwithdraw_router
from src.routers import bankaccount_router
from src.routers import bankdeposit_router
from src.routers import commonjournal_router
from src.routers import assignpermission_router
from src.routers import employee_router
from src.routers import user_router
from src.routers import login_router
from src.routers import role_permission_router
from src.routers import role_router
from src.routers import permission_router
from src.routers import generatesalary_router
from src.routers import payscalemappings_router
from src.routers import controlitem_router
from src.routers import reportingitem_router
from src.routers import detailitem_router
from src.routers import common_router
from src.routers import salarydetail_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# CORS setup
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tenant_router.router)
app.include_router(customerreceipt_router.router)
app.include_router(salesinvoice_router.router)
app.include_router(accountingrule_router.router)
app.include_router(quotation_router.router)
app.include_router(salesorder_router.router)
app.include_router(commondropdown_router.router)
app.include_router(banktransaction_router.router)
app.include_router(accountreport__router.router)
app.include_router(period__router.router)
app.include_router(closing_router.router)
app.include_router(trialbalance_router.router)
app.include_router(balancesheet_router.router)
app.include_router(bankwithdraw_router.router)
app.include_router(bankaccount_router.router)
app.include_router(bankdeposit_router.router)
app.include_router(commonjournal_router.router)
app.include_router(reportingitem_router.router)
app.include_router(detailitem_router.router)
app.include_router(common_router.router)
app.include_router(controlitem_router.router)
app.include_router(assignpermission_router.router)
app.include_router(login_router.router)
app.include_router(user_router.router)
app.include_router(role_permission_router.router)
app.include_router(role_router.router)
app.include_router(permission_router.router)
app.include_router(generatesalary_router.router)
app.include_router(salarydetail_router.router)
app.include_router(payscalemappings_router.router)
app.include_router(employee_router.router)

