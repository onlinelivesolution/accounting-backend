from pydantic import BaseModel, ConfigDict

class BranchDropdown(BaseModel):
    branchID: int
    branchName: str

    model_config = ConfigDict(from_attributes=True)