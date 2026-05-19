from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, BigInteger
from src.models.overtime import Overtime
from src.models.employee import Employee
from sqlalchemy.orm import relationship
from src.services.database import Base

class OvertimeDetail(Base):
    __tablename__ = "OvertimeDetail"
    
    overtimeDetailID     = Column(Integer, primary_key=True, index=True)    
    overtimeID           = Column(Integer, ForeignKey("Overtime.overtimeID"))
    employeeID           = Column(BigInteger, ForeignKey("Employee.employeeID")) 
    perHourRate          = Column(Numeric(18, 2), nullable=False)
    applicableRate       = Column(Numeric(18, 2), nullable=False)
    totalHour            = Column(Numeric(18, 2), nullable=False)
    totalAmount          = Column(Numeric(18, 2), nullable=False)
    
    overtime = relationship("Overtime", back_populates="details")
    employee = relationship("Employee", back_populates="overtime_details")
  