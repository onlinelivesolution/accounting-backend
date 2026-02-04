from pydantic import BaseModel, ConfigDict

class RoleDropdown(BaseModel):
    roleID: int
    roleName: str

    model_config = ConfigDict(from_attributes=True)