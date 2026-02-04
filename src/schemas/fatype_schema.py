from pydantic import BaseModel, ConfigDict

class FATypeDropdown(BaseModel):
    fATypeID: int
    fATypeName: str
    
    class Config:
        from_attributes = True
