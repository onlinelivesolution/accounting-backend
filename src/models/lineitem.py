from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from src.services.database import Base
from sqlalchemy.sql import func

class LineItem(Base):
    __tablename__ = "LineItem"
    
    itemID              = Column(Integer, primary_key=True, index=True) 
    itemCode            = Column(String(30), nullable=False)
    itemName            = Column(String(50), nullable=False)
    unitPrice           = Column(Numeric(18, 2))
    supplierProductCode = Column(String(50), nullable=True)
    description         = Column(String(200), nullable=True)
    productBrandID      = Column(Integer, nullable=True)
    productTypeID       = Column(Integer, nullable=True) 
    productSizeID       = Column(Integer, nullable=True) 
    productModelID      = Column(Integer, nullable=True) 
    productColorID      = Column(Integer, nullable=True) 
    packSize            = Column(String(50), nullable=True)  
    supplierID          = Column(Integer, nullable=True)   
    reorderQuantity     = Column(Numeric(18, 2))
    isRawMeterial       = Column(Boolean, default=True) 
    isFinishedProduct   = Column(Boolean, default=True)
    isActive            = Column(Boolean, default=True)
    accMasterCode       = Column(String(20), nullable=True) 
    companyCode         = Column(String(2), nullable=True) 
    activityCenterCode  = Column(String(4), nullable=True) 
    respCenterCode      = Column(String(6), nullable=True) 
    vAT                 = Column(Numeric(18, 2))
    controlItemCode     = Column(String(2), nullable=True) 
    reportingItemCode   = Column(String(4), nullable=True) 
    detailItemCode      = Column(String(6), nullable=True) 