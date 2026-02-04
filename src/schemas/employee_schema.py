from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EmployeeBase(BaseModel):
    employeeCode: str
    applicantID: int
    firstName: str
    middleName: str
    lastName: str
    employeeName: str
    fatherName: str
    motherName: str
    gender: int
    dateOfBirth: Optional[datetime] = None
    nationalID: str
    address: str
    postalAddress: str
    accountHolder: str
    bankID: int
    bankBranchID: int
    accountNumber: str
    designation: str
    joinDate: Optional[datetime] = None
    email: str
    phone: str
    companyCode: Optional[str] = None
    activityCenterCode: Optional[str] = None
    respCenterCode: Optional[str] = None
    emergencyContact: str
    status: int
    deviceID: int
    gradedTaxNo: str
    employeeSetID: int
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = datetime.utcnow()

class EmployeeCreate(EmployeeBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = datetime.utcnow()

class EmployeeUpdate(BaseModel):
    employeeID: int
    applicantID: int
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    employeeName: Optional[str] = None
    fatherName: Optional[str] = None
    motherName: Optional[str] = None
    gender: int
    dateOfBirth: Optional[datetime] = None
    nationalID: Optional[str] = None
    address: Optional[str] = None
    postalAddress: Optional[str] = None
    accountHolder: Optional[str] = None
    bankID: int
    bankBranchID: int
    accountNumber: Optional[str] = None
    designation: Optional[str] = None
    joinDate: Optional[datetime] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    emergencyContact: Optional[str] = None
    status: int
    deviceID: int
    gradedTaxNo: Optional[str] = None
    employeeSetID: int
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = datetime.utcnow()

class EmployeeRead(EmployeeBase):
    createdBy: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedBy: Optional[str] = None
    updatedDate: Optional[datetime] = None
    isDeleted: Optional[bool] = False

    class Config:
        from_attributes = True
        
        
