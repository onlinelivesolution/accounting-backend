from pydantic import BaseModel, ConfigDict

class DropdownItem(BaseModel):
    id: int
    name: str

class LineItemDropdown(BaseModel):
    itemID: int
    itemName: str
    itemCode: str
    unitPrice: float

    class Config:
        from_attributes = True

class CustomerDropdown(BaseModel):
    customerID: int
    customerName: str
    vatReference: str
    creditLimit: float

    class Config:
        from_attributes = True