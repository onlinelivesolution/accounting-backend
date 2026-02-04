from pydantic import BaseModel, ConfigDict

class BankDropdown(BaseModel):
    bankID: int
    bankName: str

    model_config = ConfigDict(from_attributes=True)