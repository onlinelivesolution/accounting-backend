from pydantic import BaseModel

class AccountTypeDropdown(BaseModel):
    accountTypeID: int
    accountTypeName: str
    
    class Config:
        from_attributes = True