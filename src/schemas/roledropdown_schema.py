from pydantic import BaseModel

class RoleDropdown(BaseModel):
    roleID: int
    roleName: str
    
    class Config:
        from_attributes = True