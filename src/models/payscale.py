from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from src.services.database import Base


class PayScale(Base):
    __tablename__ = "PayScale"

    payscaleID           = Column(Integer, primary_key=True, index=True)
    employeeID           = Column(BigInteger, ForeignKey('Employee.employeeID'))    
    payscaleName         = Column(String(50), nullable=True)
    payGrade             = Column(String(20), nullable=True)
    companyCode          = Column(String(2), nullable=True)
    createdBy            = Column(String(50), nullable=True)
    createdDate          = Column(DateTime, nullable=True)
    updatedBy            = Column(String(50), nullable=True)
    updatedDate          = Column(DateTime, nullable=True)
    status               = Column(Integer, nullable=True)


    mappings = relationship("PayScaleMapping", back_populates="payscale")
    employee = relationship("Employee", back_populates="payscales")

