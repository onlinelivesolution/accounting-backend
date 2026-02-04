from pydantic import BaseModel, ConfigDict

class ResponsibilityCenterDTO(BaseModel):
    respCenterCode: str
    respCenterName: str

    model_config = ConfigDict(from_attributes=True)