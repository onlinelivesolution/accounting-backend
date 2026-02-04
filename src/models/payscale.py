from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.services.database import Base


class PayScale(Base):
    __tablename__ = "PayScale"

    payscaleID           = Column(Integer, primary_key=True, index=True)
    employeeID           = Column(Integer, ForeignKey('Employee.employeeID'))    
    payscaleName         = Column(String(50), nullable=False)
    payGrade             = Column(String(20), nullable=False)
    companyCode          = Column(String(2), nullable=False)
    createdBy            = Column(String(50), nullable=False)
    createdDate          = Column(DateTime, nullable=False)
    updatedBy            = Column(String(50), nullable=False)
    updatedDate          = Column(DateTime, nullable=False)
    status               = Column(Integer, nullable=False)


    mappings = relationship("PayScaleMapping", back_populates="payscale")
    employee = relationship("Employee", back_populates="payscales")

