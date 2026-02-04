from pydantic import BaseModel, ConfigDict

class ActivityCenterDTO(BaseModel):
    activityCenterCode: str
    activityCenterName: str

    model_config = ConfigDict(from_attributes=True)