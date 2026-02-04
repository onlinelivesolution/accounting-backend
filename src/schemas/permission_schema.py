from pydantic import BaseModel

class PermissionActionInfo(BaseModel):
    permissionID: int
    permissionName: str
    actionName: str
    isAllowed: bool
    
    class Config:
        from_attributes = True