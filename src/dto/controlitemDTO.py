from pydantic import BaseModel, ConfigDict

class ControlItemDropdown(BaseModel):
    controlItemCode: str
    controlItemName: str

    model_config = ConfigDict(from_attributes=True)