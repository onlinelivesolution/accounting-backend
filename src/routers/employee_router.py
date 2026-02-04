from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from src.services.employee_service import IEmployeeService
from src.depends.service_depends import get_employee_service
from src.schemas.employee_schema import EmployeeRead, EmployeeCreate, EmployeeUpdate
from fastapi import APIRouter, Depends, File, UploadFile
from src.depends.service_depends import get_employee_service
from src.services.interfaces.iemployee_service import IEmployeeService
from fastapi.responses import JSONResponse
import json

router = APIRouter(prefix="/api/employees", tags=["Employees"])

@router.post("/addEmployee")
async def add_employee(
    employee: EmployeeCreate,
    service: IEmployeeService = Depends(get_employee_service)
):
    return await service.add_employee(employee)

@router.put("/updateEmployee/{employeeCode}", response_model=EmployeeRead)
async def update_employee(
    employeeCode: str,
    employee: EmployeeUpdate,
    service: IEmployeeService = Depends(get_employee_service),
):
    updated_item = await service.update_employee(employeeCode, employee)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_item

@router.get("/lastEmployeeCode")
async def generate_next_employee_code(service: IEmployeeService = Depends(get_employee_service)):
    """
    Returns the highest (last) employeeCode from the Employee table.
    Example response: { "lastEmployeeCode": "00105" }
    """
    last_code = await service.generate_next_employee_code()
    if last_code is None:
        return {"lastEmployeeCode": None}

    return {"lastEmployeeCode": last_code}

@router.get("/employeeTable", response_model=List[EmployeeRead])
async def get_all_active_employees(
    skip: int = 0,
    limit: int = 100,
    service: IEmployeeService = Depends(get_employee_service)
):
    return await service.get_all_active_employees()

class NaNJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            content,
            allow_nan=True,   # 👈 allow NaN, Infinity, -Infinity
            default=str
        ).encode("utf-8")

@router.get("/loadEmployeeForPayScaleMapping")
async def get_all_employees(service: IEmployeeService = Depends(get_employee_service)):
    return await service.get_all_employees() 

@router.get("/loadAllInformationFromEmployeeTable")
async def get_all_employee_information(service: IEmployeeService = Depends(get_employee_service)):
    return await service.get_all_employee_information()  

@router.post("/uploadEmployeeCSVFile")
async def upload_employees_csv(
    file: UploadFile,
    service: IEmployeeService = Depends(get_employee_service)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    result = await service.upload_employees_csv(file)
    return {"message": "Employees uploaded successfully", "inserted": result}
    


