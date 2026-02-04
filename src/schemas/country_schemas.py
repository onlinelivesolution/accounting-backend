from pydantic import BaseModel, ConfigDict

class CountryDropdown(BaseModel):
    countryID: int
    countryName: str

    model_config = ConfigDict(from_attributes=True)